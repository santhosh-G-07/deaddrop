from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Max
from .models import Message, Room, RoomVisit, Task, TaskUpdate
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
    rooms = Room.objects.all()
    
    room_data = []
    for room in rooms:
        try:
            visit = RoomVisit.objects.get(room_code=room.code, session_key=session_key)
            last_visit = visit.last_visit
        except RoomVisit.DoesNotExist:
            last_visit = None
        
        if last_visit:
            if room.room_type == 'chat':
                unread_count = Message.objects.filter(
                    room_code=room.code,
                    created_at__gt=last_visit
                ).count()
            else:  # task room
                unread_count = TaskUpdate.objects.filter(
                    task__room_code=room.code,
                    created_at__gt=last_visit
                ).count()
        else:
            if room.room_type == 'chat':
                unread_count = Message.objects.filter(room_code=room.code).count()
            else:
                unread_count = TaskUpdate.objects.filter(task__room_code=room.code).count()
        
        last_message = None
        if room.room_type == 'chat':
            last_msg = Message.objects.filter(room_code=room.code).last()
            if last_msg:
                last_message = last_msg.created_at.isoformat()
        else:
            last_task = Task.objects.filter(room_code=room.code).last()
            if last_task:
                last_message = last_task.updated_at.isoformat()
        
        room_data.append({
            'code': room.code,
            'name': room.name,
            'room_type': room.room_type,
            'unread_count': unread_count,
            'last_message_time': last_message,
            'created_at': room.created_at.isoformat()
        })
    
    return JsonResponse({'rooms': room_data})


def validate_code(request):
    """Validate room code and check if master code needed for new rooms"""
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        master = request.POST.get('master', '').strip()
        room_name = request.POST.get('room_name', '').strip()
        room_type = request.POST.get('room_type', 'chat').strip()
        
        if not code or len(code) < 4:
            return JsonResponse({'success': False, 'error': 'Code too short'})
        
        try:
            room = Room.objects.get(code=code)
            request.session['authenticated'] = True
            request.session['room_code'] = code
            request.session['room_type'] = room.room_type
            return JsonResponse({'success': True, 'exists': True, 'room_type': room.room_type})
        except Room.DoesNotExist:
            if master != MASTER_CODE:
                return JsonResponse({
                    'success': False, 
                    'error': 'Master code required for new room',
                    'need_master': True
                })
            
            if not room_name:
                room_name = f"Room {code}"
            
            Room.objects.create(code=code, name=room_name, room_type=room_type)
            request.session['authenticated'] = True
            request.session['room_code'] = code
            request.session['room_type'] = room_type
            return JsonResponse({'success': True, 'exists': False, 'created': True, 'room_type': room_type})
    
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
    """Main message board - shows messages from last 24 hours only"""
    if not request.session.get('authenticated'):
        return redirect('landing')
    
    room_code = request.session.get('room_code')
    room_type = request.session.get('room_type', 'chat')
    
    if not room_code:
        return redirect('landing')
    
    # Redirect to task board if it's a task room
    if room_type == 'task':
        return redirect('task_board')
    
    room, created = Room.objects.get_or_create(
        code=room_code,
        defaults={'name': f'Room {room_code}', 'room_type': 'chat'}
    )
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(
                room_code=room_code,
                text=text
            )
            return redirect('board')
    
    from datetime import timedelta
    last_24_hours = timezone.now() - timedelta(hours=24)
    messages = Message.objects.filter(
        room_code=room_code,
        created_at__gte=last_24_hours
    )
    
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


def task_board(request):
    """Task management board - tasks stay forever"""
    if not request.session.get('authenticated'):
        return redirect('landing')
    
    room_code = request.session.get('room_code')
    if not room_code:
        return redirect('landing')
    
    room, created = Room.objects.get_or_create(
        code=room_code,
        defaults={'name': f'Room {room_code}', 'room_type': 'task'}
    )
    
    # Get all tasks grouped by due date
    tasks = Task.objects.filter(room_code=room_code).order_by('-created_at')
    
    if not request.session.session_key:
        request.session.create()
    
    RoomVisit.objects.update_or_create(
        room_code=room_code,
        session_key=request.session.session_key,
        defaults={'last_visit': timezone.now()}
    )
    
    context = {
        'tasks': tasks,
        'room_code': room_code,
        'room_name': room.name,
    }
    return render(request, 'board/task_board.html', context)


def create_task(request):
    """Create a new task"""
    if request.method == 'POST':
        room_code = request.session.get('room_code')
        if not room_code:
            return JsonResponse({'success': False, 'error': 'Not authenticated'})
        
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date', '')
        
        if not title:
            return JsonResponse({'success': False, 'error': 'Title required'})
        
        task = Task.objects.create(
            room_code=room_code,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date if due_date else None
        )
        
        return JsonResponse({'success': True, 'task_id': task.id})
    
    return JsonResponse({'success': False})


def update_task_status(request):
    """Update task status"""
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')
        
        try:
            task = Task.objects.get(id=task_id)
            task.status = status
            task.save()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
    
    return JsonResponse({'success': False})


def add_task_update(request):
    """Add update/comment to task"""
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        text = request.POST.get('text', '').strip()
        
        if not text:
            return JsonResponse({'success': False, 'error': 'Text required'})
        
        try:
            task = Task.objects.get(id=task_id)
            TaskUpdate.objects.create(task=task, text=text)
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
    
    return JsonResponse({'success': False})


def check_new_messages(request):
    """Check for new messages in current room (for notifications)"""
    if not request.session.get('authenticated'):
        return JsonResponse({'has_new': False})
    
    room_code = request.session.get('room_code')
    if not room_code:
        return JsonResponse({'has_new': False})
    
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
    
    request.session['last_message_check'] = timezone.now().isoformat()
    
    return JsonResponse({
        'has_new': new_count > 0,
        'count': new_count
    })


def logout_view(request):
    """Clear session and redirect to landing"""
    request.session.flush()
    return redirect('landing')
