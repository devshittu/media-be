from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'report_type', 'created_at']
    list_filter = ['report_type', 'created_at']
    search_fields = ['user__email', 'description']
