from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from attendance.forms import AttendanceForm, InternshipForm
from attendance.models import AttendanceModel, InternshipModel
from background_task import background
from django.contrib.auth.models import User
from project.models import Project


@login_required(login_url='/login/')
def attendanceView(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = AttendanceModel()
            attendance.name = form.cleaned_data['name']
            attendance.date = form.cleaned_data['date']
            attendance.save()
            return redirect('myattendance')
    else:
        form = AttendanceForm(initial={"name": request.user.username})
    return render(request, 'attendance.html', {'form': form})


@login_required(login_url='/login/')
def AttendanceCounter(request):
    response = Internship(request)
    attendance_user = AttendanceModel.objects.filter(name=request.user)
    return render(request, 'attendance_counter.html', {'attendances': attendance_user})


@login_required(login_url='/login/')
def Internship(request):
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            internship = InternshipModel()
            internship.period = form.cleaned_data['period']
            internship.name = form.cleaned_data['name']
            internship.save()
            return redirect('myattendance')
    else:
        form = InternshipForm(initial={"name": request.user.username})

    return render(request, 'internship_period.html', {'form': form})
