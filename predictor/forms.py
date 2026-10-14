from django import forms
from .models import StudyRecord

class StudyHabitForm(forms.ModelForm):
    class Meta:
        model = StudyRecord
        fields = [
            "subject",
            "time_of_day",
            "study_hours_per_day",
            "sleep_hours",
            "phone_usage_hours",
            "attendance_percentage",
            "assignments_completed",
            "stress_level",
            "gender",
        ]
        labels = {
            "subject": "What did you study?",
            "time_of_day": "When did you study?",
            "study_hours_per_day": "How many hours did you study today?",
            "sleep_hours": "How many hours did you sleep last night?",
            "phone_usage_hours": "How many hours on your phone today?",
            "attendance_percentage": "Your attendance so far (%)",
            "assignments_completed": "Assignments completed",
            "stress_level": "Stress level today (1 = calm, 10 = overwhelmed)",
            "gender": "Gender",
        }
        widgets = {
            "study_hours_per_day": forms.NumberInput(attrs={"step": "0.1", "min": 0, "max": 24}),
            "sleep_hours": forms.NumberInput(attrs={"step": "0.1", "min": 0, "max": 24}),
            "phone_usage_hours": forms.NumberInput(attrs={"step": "0.1", "min": 0, "max": 24}),
            "attendance_percentage": forms.NumberInput(attrs={"step": "0.1", "min": 0, "max": 100}),
            "assignments_completed": forms.NumberInput(attrs={"min": 0}),
            "stress_level": forms.NumberInput(attrs={"min": 1, "max": 10}),
        }

from django import forms
from django.contrib.auth.models import User
from .models import StudyRecord

class StudyHabitForm(forms.ModelForm):

    class Meta:
        model = StudyRecord
        fields = [
            "subject", "time_of_day", "study_hours_per_day", "sleep_hours",
            "phone_usage_hours", "attendance_percentage", "assignments_completed",
            "stress_level", "gender",
        ]
        labels = {
            "subject": "What did you study?",
            "time_of_day": "When did you study?",
            "study_hours_per_day": "How many hours did you study today?",
            "sleep_hours": "How many hours did you sleep last night?",
            "phone_usage_hours": "How many hours on your phone today?",
            "attendance_percentage": "Your attendance so far (%)",
            "assignments_completed": "Assignments completed",
            "stress_level": "Stress level today (1 = calm, 10 = overwhelmed)",
            "gender": "Gender",
        }
        widgets = {
            "study_hours_per_day": forms.NumberInput(attrs={"step": "0.1", "min": 0, "max": 24}),
            "sleep_hours": forms.NumberInput(attrs={"step": "0.1", "min": 0, "max": 24}),
            "phone_usage_hours": forms.NumberInput(attrs={"step": "0.1", "min": 0, "max": 24}),
            "attendance_percentage": forms.NumberInput(attrs={"step": "0.1", "min": 0, "max": 100}),
            "assignments_completed": forms.NumberInput(attrs={"min": 0}),
            "stress_level": forms.NumberInput(attrs={"min": 1, "max": 10}),
        }


class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        existing = User.objects.filter(username=username).exclude(pk=self.instance.pk)
        if existing.exists():
            raise forms.ValidationError("That username is already taken.")
        return username



    