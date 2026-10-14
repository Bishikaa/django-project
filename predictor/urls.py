from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("log/", views.predict_view, name="predict"),
    path("delete/<int:record_id>/", views.delete_record_view, name="delete_record"),
    path("export/", views.export_csv_view, name="export_csv"),
    path("profile/", views.profile_view, name="profile"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="predictor/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
]