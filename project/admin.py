# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from project.models import Project, ProgrammingLanguage

admin.site.register(Project)
admin.site.register(ProgrammingLanguage)
