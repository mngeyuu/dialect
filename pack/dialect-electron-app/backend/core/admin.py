from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DialectWord


@admin.register(DialectWord)
class DialectWordAdmin(admin.ModelAdmin):
    list_display = ('code', 'word', 'old_dialect_word', 'new_dialect_word', 'has_old_audio', 'has_new_audio')
    search_fields = ('code', 'word', 'old_dialect_word', 'new_dialect_word')
    list_filter = ('created_at',)

    def has_old_audio(self, obj):
        return bool(obj.old_dialect_audio)

    has_old_audio.boolean = True
    has_old_audio.short_description = "老派音频"

    def has_new_audio(self, obj):
        return bool(obj.new_dialect_audio)

    has_new_audio.boolean = True
    has_new_audio.short_description = "新派音频"