from django.shortcuts import render
from .forms import StudyHabitForm
from .ml_utils import predict_productivity
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Avg
from .models import StudyRecord
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
import json

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login right after signup
            return redirect("predict")
    else:
        form = UserCreationForm()
    return render(request, "predictor/signup.html", {"form": form})

@login_required
def predict_view(request):
    result = None

    if request.method == "POST":
        form = StudyHabitForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)  # don't hit the DB yet, we need the prediction first
            record.user = request.user

            score, level = predict_productivity(
                study_hours=record.study_hours_per_day,
                sleep_hours=record.sleep_hours,
                phone_hours=record.phone_usage_hours,
                attendance=record.attendance_percentage,
                assignments=record.assignments_completed,
                stress=record.stress_level,
                gender=record.gender,
            )

            record.predicted_score = score
            record.productivity_level = level
            record.save()  # now it actually goes into the database

            result = {"score": score, "level": level}
            form = StudyHabitForm()  # reset to a blank form after a successful submission
    else:
        form = StudyHabitForm()

    return render(request, "predictor/predict.html", {"form": form, "result": result})


# @login_required
def dashboard_view(request):
    records = StudyRecord.objects.filter(user=request.user).order_by("-created_at")

    if not records.exists():
        return render(request, "predictor/dashboard.html", {"has_data": False})

    overall = records.aggregate(
        avg_score=Avg("predicted_score"),
        avg_study=Avg("study_hours_per_day"),
        avg_sleep=Avg("sleep_hours"),
    )

    # group by subject, find which one has the highest average score
    subject_stats = (
        records.values("subject")
        .annotate(avg_score=Avg("predicted_score"))
        .order_by("-avg_score")
    )
    best_subject = subject_stats.first()

    subject_labels = [s["subject"] for s in subject_stats]
    subject_scores = [round(s["avg_score"], 1) for s in subject_stats]

    # group by time of day, same idea
    time_stats = (
        records.values("time_of_day")
        .annotate(avg_score=Avg("predicted_score"))
        .order_by("-avg_score")
    )
    best_time = time_stats.first()

    latest = records.first()  # most recent session, already has its own prediction

    score_diff = None
    if latest and overall["avg_score"] is not None:
        score_diff = round(latest.predicted_score - overall["avg_score"], 1)

    # a simple, honest insight: compare avg score when sleep < 6 vs >= 6
    low_sleep_avg = records.filter(sleep_hours__lt=6).aggregate(a=Avg("predicted_score"))["a"]
    ok_sleep_avg = records.filter(sleep_hours__gte=6).aggregate(a=Avg("predicted_score"))["a"]

        # Option 1: student's own best sessions
    high_sessions = records.filter(productivity_level="High")
    best_pattern = None
    if high_sessions.exists():
        best_pattern = high_sessions.aggregate(
            avg_study=Avg("study_hours_per_day"),
            avg_sleep=Avg("sleep_hours"),
            avg_phone=Avg("phone_usage_hours"),
        )

    # Option 2: static coefficient insights from the trained model (see Colab Step 6)
    coefficient_insights = [
        "Each extra hour of study adds about +11.5 points to your predicted productivity.",
        "Each extra hour of sleep adds about +5.5 points.",
        "Each extra hour on your phone costs about -5 points.",
        "Each 10% increase in attendance adds about +28.5 points.",
    ]

    chart_records = list(records.order_by("created_at")[:20])  # oldest to newest, last 20
    chart_labels = [r.created_at.strftime("%b %d, %H:%M") for r in chart_records]
    chart_scores = [r.predicted_score for r in chart_records]
    context = {
        "has_data": True,
        "overall": overall,
        "best_subject": best_subject,
        "best_time": best_time,
        "latest": latest,
        "low_sleep_avg": low_sleep_avg,
        "ok_sleep_avg": ok_sleep_avg,
        "history": records[:10],
        "best_pattern": best_pattern,
        "coefficient_insights": coefficient_insights,
        "chart_labels": json.dumps(chart_labels),
        "chart_scores": json.dumps(chart_scores),
        "subject_labels": json.dumps(subject_labels),
        "subject_scores": json.dumps(subject_scores),
        "score_diff": score_diff,
    }
    return render(request, "predictor/dashboard.html", context)



@login_required
@require_POST
def delete_record_view(request, record_id):
    record = get_object_or_404(StudyRecord, id=record_id, user=request.user)
    record.delete()
    return redirect("dashboard")

import csv
from django.http import HttpResponse

@login_required
def export_csv_view(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="studywise_history.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date", "Subject", "Time of Day", "Study Hours", "Sleep Hours",
                      "Phone Usage", "Attendance %", "Assignments", "Stress Level",
                      "Predicted Score", "Productivity Level"])

    records = StudyRecord.objects.filter(user=request.user).order_by("-created_at")
    for r in records:
        writer.writerow([r.created_at.strftime("%Y-%m-%d %H:%M"), r.subject, r.time_of_day,
                          r.study_hours_per_day, r.sleep_hours, r.phone_usage_hours,
                          r.attendance_percentage, r.assignments_completed, r.stress_level,
                          r.predicted_score, r.productivity_level])
    return response

from datetime import timedelta
from django.utils import timezone

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import StudyHabitForm, UsernameChangeForm

@login_required
def profile_view(request):
    records = StudyRecord.objects.filter(user=request.user).order_by("-created_at")
    total_sessions = records.count()

    logged_dates = sorted(set(r.created_at.date() for r in records), reverse=True)
    streak = 0
    if logged_dates:
        expected = timezone.now().date()
        for d in logged_dates:
            if d == expected:
                streak += 1
                expected -= timedelta(days=1)
            elif d == expected + timedelta(days=1):
                continue
            else:
                break

    hour = timezone.localtime().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    if streak == 0:
        streak_message = "No active streak yet, log a session today to start one!"
    elif streak == 1:
        streak_message = "You're just getting started, keep it up tomorrow!"
    elif streak < 5:
        streak_message = "Nice, you're building a habit."
    else:
        streak_message = "You're on fire, this is becoming a real routine."

    username_form = UsernameChangeForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == "POST":
        if "update_username" in request.POST:
            username_form = UsernameChangeForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, "Username updated.")
                return redirect("profile")

        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated.")
                return redirect("profile")

    context = {
        "total_sessions": total_sessions,
        "streak": streak,
        "streak_message": streak_message,
        "member_since": request.user.date_joined,
        "greeting": greeting,
        "username_form": username_form,
        "password_form": password_form,
    }
    return render(request, "predictor/profile.html", context)