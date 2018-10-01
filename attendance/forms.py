from django import forms
from django.forms import ModelForm

from attendance.models import AttendanceModel, InternshipModel


class AttendanceForm(ModelForm):
    class Meta:
        model = AttendanceModel
        fields = ('name', 'date')


class InternshipForm(ModelForm):
    class Meta:
        model = InternshipModel
        fields = ('name', 'period')
