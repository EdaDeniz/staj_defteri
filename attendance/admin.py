# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from attendance.models import AttendanceModel, InternshipModel


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')

class InternshipAdmn(admin.ModelAdmin):
    list_display = ('name', 'period',)


admin.site.register(AttendanceModel, AttendanceAdmin)
admin.site.register(InternshipModel, InternshipAdmn)