from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room_code', 'text_preview', 'created_at']
    list_filter = ['room_code', 'created_at']
    search_fields = ['text', 'room_code']
    readonly_fields = ['created_at']
    
    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'Message'

