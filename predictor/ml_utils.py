import os
import joblib
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_model", "studywise_model.pkl")
_model = None  # loaded once, reused for every request

def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def productivity_level(score):
    if score >= 60:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"

def predict_productivity(study_hours, sleep_hours, phone_hours, attendance, assignments, stress, gender):
    import pandas as pd
    model = get_model()
    row = pd.DataFrame([{
        "study_hours_per_day": study_hours,
        "sleep_hours": sleep_hours,
        "phone_usage_hours": phone_hours,
        "attendance_percentage": attendance,
        "assignments_completed": assignments,
        "stress_level": stress,
        "gender": gender,
    }])
    score = float(model.predict(row)[0])
    score = max(0.0, min(100.0, score))  # keep it in a sensible range
    return round(score, 2), productivity_level(score)