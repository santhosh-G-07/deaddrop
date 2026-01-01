from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Message
import os
from dotenv import load_dotenv

load_dotenv()


def landing(request):
    """Black landing page with minimal UI"""
    return render(request, 'board/landing.html')


def validate_code(request):
    """Validate and store any access code - each code creates a unique room"""
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        
        # Accept any non-empty code (minimum 4 characters for security)
        if code and len(code) >= 4:
            request.session['authenticated'] = True
            request.session['room_code'] = code  # Store the room code
            return JsonResponse({'success': True})
        
        return JsonResponse({'success': False})
    return JsonResponse({'success': False})


def board(request):
    """Main message board - shows only messages from current room"""
    if not request.session.get('authenticated'):
        return redirect('landing')
    
    room_code = request.session.get('room_code')
    if not room_code:
        return redirect('landing')
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(
                room_code=room_code,
                text=text
            )
            return redirect('board')
    
    # Get today's messages for THIS ROOM ONLY
    today = timezone.now().date()
    messages = Message.objects.filter(
        room_code=room_code,
        created_at__date=today
    )
    
    context = {
        'messages': messages,
        'today': today,
        'room_code': room_code,  # Pass room code to template
    }
    return render(request, 'board/board.html', context)


def logout_view(request):
    """Clear session and redirect to landing"""
    request.session.flush()
    return redirect('landing')

