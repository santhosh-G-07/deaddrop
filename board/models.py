from django.db import models


class Message(models.Model):
    room_code = models.CharField(max_length=50, db_index=True)  # Room identifier
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['room_code', 'created_at']),
        ]
    
    def __str__(self):
        return f"[{self.room_code}] {self.text[:50]}... ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
