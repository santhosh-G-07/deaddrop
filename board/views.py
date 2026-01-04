from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Max
from .models import Message, Room, RoomVisit
import os
from dotenv import load_dotenv

load_dotenv()

MASTER_CODE = os.getenv('MASTER_CODE', '7777')


def landing(request):
    """UPSC educational article landing page"""
    return render(request, 'board/landing.html')


def get_room_list(request):
    """Get list of all rooms with unread counts for current session"""
    if not request.session.session_key:
        request.session.create()
    
    session_key = request.session.session_key
    
    # Get all rooms
    rooms = Room.objects.all()
    
    room_data = []
    for room in rooms:
        # Get last visit time for this session
        try:
            visit = RoomVisit.objects.get(room_code=room.code, session_key=session_key)
            last_visit = visit.last_visit
        except RoomVisit.DoesNotExist:
            last_visit = None
        
        # Count unread messages
        if last_visit:
            unread_count = Message.objects.filter(
                room_code=room.code,
                created_at__gt=last_visit
            ).count()
        else:
            unread_count = Message.objects.filter(room_code=room.code).count()
        
        # Get last message time
        last_message = Message.objects.filter(room_code=room.code).last()
        
        room_data.append({
            'code': room.code,
            'name': room.name,
            'unread_count': unread_count,
            'last_message_time': last_message.created_at.isoformat() if last_message else None,
            'created_at': room.created_at.isoformat()
        })
    
    return JsonResponse({'rooms': room_data})


def validate_code(request):
    """Validate room code and check if master code needed for new rooms"""
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        master = request.POST.get('master', '').strip()
        room_name = request.POST.get('room_name', '').strip()
        
        # Minimum 4 characters
        if not code or len(code) < 4:
            return JsonResponse({'success': False, 'error': 'Code too short'})
        
        # Check if room exists
        try:
            room = Room.objects.get(code=code)
            # Room exists, no master code needed
            request.session['authenticated'] = True
            request.session['room_code'] = code
            return JsonResponse({'success': True, 'exists': True})
        except Room.DoesNotExist:
            # New room - need master code
            if master != MASTER_CODE:
                return JsonResponse({
                    'success': False, 
                    'error': 'Master code required for new room',
                    'need_master': True
                })
            
            # Create new room
            if not room_name:
                room_name = f"Room {code}"
            
            Room.objects.create(code=code, name=room_name)
            request.session['authenticated'] = True
            request.session['room_code'] = code
            return JsonResponse({'success': True, 'exists': False, 'created': True})
    
    return JsonResponse({'success': False})


def update_room_name(request):
    """Update room name"""
    if request.method == 'POST':
        room_code = request.POST.get('room_code', '').strip()
        new_name = request.POST.get('new_name', '').strip()
        
        if not room_code or not new_name:
            return JsonResponse({'success': False, 'error': 'Missing data'})
        
        try:
            room = Room.objects.get(code=room_code)
            room.name = new_name
            room.save()
            return JsonResponse({'success': True})
        except Room.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Room not found'})
    
    return JsonResponse({'success': False})


def board(request):
    """Main message board - shows ALL messages from current room"""
    if not request.session.get('authenticated'):
        return redirect('landing')
    
    room_code = request.session.get('room_code')
    if not room_code:
        return redirect('landing')
    
    # Get or create room
    room, created = Room.objects.get_or_create(
        code=room_code,
        defaults={'name': f'Room {room_code}'}
    )
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(
                room_code=room_code,
                text=text
            )
            return redirect('board')
    
    # Get ALL messages for THIS ROOM (messages persist forever)
    messages = Message.objects.filter(room_code=room_code)
    
    # Update last visit time for unread tracking
    if not request.session.session_key:
        request.session.create()
    
    RoomVisit.objects.update_or_create(
        room_code=room_code,
        session_key=request.session.session_key,
        defaults={'last_visit': timezone.now()}
    )
    
    context = {
        'messages': messages,
        'room_code': room_code,
        'room_name': room.name,
    }
    return render(request, 'board/board.html', context)


def check_new_messages(request):
    """Check for new messages in current room (for notifications)"""
    if not request.session.get('authenticated'):
        return JsonResponse({'has_new': False})
    
    room_code = request.session.get('room_code')
    if not room_code:
        return JsonResponse({'has_new': False})
    
    # Get last check time from session
    last_check = request.session.get('last_message_check')
    
    if last_check:
        from datetime import datetime
        last_check_time = datetime.fromisoformat(last_check)
        new_count = Message.objects.filter(
            room_code=room_code,
            created_at__gt=last_check_time
        ).count()
    else:
        new_count = 0
    
    # Update last check time
    request.session['last_message_check'] = timezone.now().isoformat()
    
    return JsonResponse({
        'has_new': new_count > 0,
        'count': new_count
    })


def logout_view(request):
    """Clear session and redirect to landing"""
    request.session.flush()
    return redirect('landing')
