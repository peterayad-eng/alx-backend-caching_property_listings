from django.contrib import admin
from .models import Property

# Register your models here.
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'price', 'created_at']
    list_filter = ['location', 'created_at']
    search_fields = ['title', 'location', 'description']
    ordering = ['-created_at']

