from django.db import models
from django.contrib.auth.models import User

class StudyRecord(models.Model):
    GENDER_CHOICES = [
        ("Female", "Female"),
        ("Male", "Male"),
        ("Other", "Other"),
    ]
    SUBJECT_CHOICES = [
        ("Math", "Math"), ("DSA", "DSA"), ("Physics", "Physics"),
        ("Programming", "Programming"), ("English", "English"), ("Other", "Other"),
    ]
    TIME_OF_DAY_CHOICES = [
        ("Morning", "Morning (6AM–12PM)"),
        ("Afternoon", "Afternoon (12PM–5PM)"),
        ("Evening", "Evening (5PM–9PM)"),
        ("Night", "Night (9PM–6AM)"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="study_records")

    study_hours_per_day = models.FloatField()
    sleep_hours = models.FloatField()
    phone_usage_hours = models.FloatField()
    attendance_percentage = models.FloatField()
    assignments_completed = models.IntegerField()
    stress_level = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default="Other")
    time_of_day = models.CharField(max_length=10, choices=TIME_OF_DAY_CHOICES, default="Evening")

    predicted_score = models.FloatField()
    productivity_level = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.created_at:%Y-%m-%d %H:%M} — {self.predicted_score}"