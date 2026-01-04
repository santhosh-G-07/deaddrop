from django.contrib import admin
from .models import Message, Room, RoomVisit


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'message_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at']
    
    def message_count(self, obj):
        return Message.objects.filter(room_code=obj.code).count()
    message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room_code', 'text_preview', 'created_at']
    list_filter = ['room_code', 'created_at']
    search_fields = ['text', 'room_code']
    readonly_fields = ['created_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Message'


@admin.register(RoomVisit)
class RoomVisitAdmin(admin.ModelAdmin):
    list_display = ['room_code', 'session_key_preview', 'last_visit']
    list_filter = ['room_code', 'last_visit']
    search_fields = ['room_code', 'session_key']
    readonly_fields = ['last_visit']
    
    def session_key_preview(self, obj):
        return obj.session_key[:20] + '...' if len(obj.session_key) > 20 else obj.session_key
    session_key_preview.short_description = 'Session'
