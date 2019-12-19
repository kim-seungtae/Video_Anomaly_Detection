from django.urls import path
from . import views

app_name = "tower"

urlpatterns = [
    path('', views.main, name="main"),
    path('report/<int:pk>', views.report, name="report"),
    path('report_list/<int:pk>', views.report_list, name="report_list"),
    path('register/', views.register, name="register"),
]