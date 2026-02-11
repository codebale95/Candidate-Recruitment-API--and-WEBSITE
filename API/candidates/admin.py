from django.contrib import admin
from .models import User, Candidate

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active']

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'role', 'stage', 'created_at']
    list_filter = ['stage', 'created_at']
    search_fields = ['name', 'email', 'role']
    readonly_fields = ['created_at', 'updated_at']
