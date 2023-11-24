from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Desk, Leg

@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image_display']
    
    def image_display(self, obj):
        if obj.image:
            # Use mark_safe to mark the following string as safe HTML content
            return mark_safe('<img src="{}" width="150" />'.format(obj.image.url))
        return "No Image"
    image_display.short_description = 'Image'
    
    readonly_fields = ['image_display',]

@admin.register(Leg)
class LegAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image_display']
    
    def image_display(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" width="150" />'.format(obj.image.url))
        return "No Image"
    image_display.short_description = 'Image'
    
    readonly_fields = ['image_display',]
