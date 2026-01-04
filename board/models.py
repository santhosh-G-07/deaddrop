from django.db import models


class Room(models.Model):
    """Room with custom name and code"""
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=100, default="Unnamed Room")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_unread_count(self, last_visit=None):
        """Get count of messages since last visit"""
        if not last_visit:
            return self.messages.count()
        return self.messages.filter(created_at__gt=last_visit).count()


class Message(models.Model):
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
