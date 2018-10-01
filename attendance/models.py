# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models
from singleton_model import SingletonModel


class AttendanceModel(models.Model):
    name = models.CharField(max_length=100, default=User)
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = ('name', 'date',)


class InternshipModel(SingletonModel):
    name = models.CharField(max_length=100, default=User)
    period = models.IntegerField()

