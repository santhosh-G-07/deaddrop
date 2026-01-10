from django.db import models


class Room(models.Model):
    """Room with custom name and code"""
    ROOM_TYPES = (
        ('chat', 'Chat Room'),
        ('task', 'Task Room'),
    )
    
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=100, default="Unnamed Room")
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='chat')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.room_type})"
    
    def get_unread_count(self, last_visit=None):
        """Get count of messages since last visit"""
        if not last_visit:
            return self.messages.count()
        return self.messages.filter(created_at__gt=last_visit).count()


class Message(models.Model):
    """Chat messages - auto-delete after 24 hours"""
    room_code = models.CharField(max_length=50, db_index=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['room_code', 'created_at']),
        ]
    
    def __str__(self):
        return f"[{self.room_code}] {self.text[:50]}... ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class Task(models.Model):
    """Tasks - permanent, never delete"""
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),
        ('done', 'Done'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    
    room_code = models.CharField(max_length=50, db_index=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['room_code', 'due_date']),
            models.Index(fields=['room_code', 'status']),
        ]
    
    def __str__(self):
        return f"[{self.room_code}] {self.title}"


class TaskUpdate(models.Model):
    """Updates/comments on tasks - permanent"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='updates')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.task.title} - {self.text[:30]}..."


class RoomVisit(models.Model):
    """Track when user last visited each room (for unread indicators)"""
    room_code = models.CharField(max_length=50, db_index=True)
    session_key = models.CharField(max_length=100)
    last_visit = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['room_code', 'session_key']
        indexes = [
            models.Index(fields=['session_key', 'room_code']),
        ]
    
    def __str__(self):
        return f"{self.room_code} - {self.last_visit}"
