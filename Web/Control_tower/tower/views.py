from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def main(request):
    return render(request, "tower/main.html")


def report_list(request, pk):
    report_list = Report.objects.filter(area_division=pk).order_by('-created_at')
    report = report_list[0]
    image_url = "image/" + str(report.area_division) + ".png"
    num = len(report_list) + 1
    return render(request, "tower/report_list.html", {'report_list': report_list, 'report': report, 'image_url': image_url, 'num': num})

def report(request, pk):
    report = Report.objects.get(pk=pk)
    return render(request, "tower/report.html", {'report': report})


def register(request):
    if request.method == 'POST':
        report_context = {
            'description': request.POST.get('description'),
            'location': request.POST.get('location'),
            'video': request.FILES['video'],
            'anomaly_division': request.POST.get('anomaly_division'),
            'area_division': request.POST.get('area_division'),
            'picture' : request.FILES['picture']
        }
        report = Report.objects.create(**report_context)
        return redirect("tower:register")
    return render(request, "tower/register.html")