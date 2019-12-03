from django.urls import path
from . import views

app_name = "tower"

urlpatterns = [
    path('', views.main, name="main"),
    path('report/', views.report, name="report"),
    path('register/', views.register, name="register"),
]