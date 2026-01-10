from django.contrib import admin
from .models import Message, Room, RoomVisit, Task, TaskUpdate


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'room_type', 'message_count', 'created_at']
    list_filter = ['room_type', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at']
    
    def message_count(self, obj):
        if obj.room_type == 'chat':
            return Message.objects.filter(room_code=obj.code).count()
        else:
            return Task.objects.filter(room_code=obj.code).count()
    message_count.short_description = 'Items'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room_code', 'text_preview', 'created_at']
    list_filter = ['room_code', 'created_at']
    search_fields = ['text', 'room_code']
    readonly_fields = ['created_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Message'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'room_code', 'status', 'priority', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'room_code', 'created_at']
    search_fields = ['title', 'description', 'room_code']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('room_code', 'title', 'description')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TaskUpdate)
class TaskUpdateAdmin(admin.ModelAdmin):
    list_display = ['task', 'text_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['text', 'task__title']
    readonly_fields = ['created_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Update'


@admin.register(RoomVisit)
class RoomVisitAdmin(admin.ModelAdmin):
    list_display = ['room_code', 'session_key_preview', 'last_visit']
    list_filter = ['room_code', 'last_visit']
    search_fields = ['room_code', 'session_key']
    readonly_fields = ['last_visit']
    
    def session_key_preview(self, obj):
        return obj.session_key[:20] + '...' if len(obj.session_key) > 20 else obj.session_key
    session_key_preview.short_description = 'Session'
