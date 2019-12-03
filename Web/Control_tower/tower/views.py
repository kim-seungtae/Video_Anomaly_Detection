from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def main(request):
    report_list = Report.objects.all().order_by('created_at')
    return render(request, "tower/main.html", {'report_list': report_list})


def report(request):
    return render(request, "tower/report.html")


def register(request):
    if request.method == 'POST':
        report_context = {
            'location': request.POST.get('location'),
            'video': request.FILES['video']
        }
        report = Report.objects.create(**report_context)
    return redirect('tower:main')