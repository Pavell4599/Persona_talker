from django.contrib import admin
from .models import Persona, RewriteRequest


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_system_persona_display', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['name', 'style_description', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'user', 'image')
        }),
        ('Описания', {
            'fields': ('style_description', 'description')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_system_persona_display(self, obj):
        return "Системная" if obj.is_system_persona() else "Пользовательская"
    is_system_persona_display.short_description = "Тип"


@admin.register(RewriteRequest)
class RewriteRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'persona', 'created_at', 'truncated_original']
    list_filter = ['persona', 'created_at', 'user']
    search_fields = ['original_text', 'rewritten_text', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    def truncated_original(self, obj):
        """Показывает первые 50 символов оригинального текста"""
        return obj.original_text[:50] + "..." if len(obj.original_text) > 50 else obj.original_text
    truncated_original.short_description = "Оригинальный текст"

