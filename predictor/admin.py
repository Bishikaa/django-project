from django.contrib import admin
from .models import StudyRecord

@admin.register(StudyRecord)
class StudyRecordAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "time_of_day", "predicted_score", "productivity_level", "created_at")
    list_filter = ("productivity_level", "subject", "time_of_day")
    search_fields = ("user__username",)