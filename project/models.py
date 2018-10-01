from __future__ import unicode_literals

import uuid
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone
from django.db import models
from singleton_model import SingletonModel
from django.contrib.auth.models import User


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(SingletonModel):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    project_name = models.CharField(max_length=300)
    project_description = RichTextField()
    project_notes = RichTextField()
    select_langs = models.ManyToManyField(ProgrammingLanguage)
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)
    slug = models.UUIDField(default=uuid.uuid4)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.project_name

    def get_delete_url(self):
        return reverse('project:delete', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('project:update', kwargs={'slug': self.slug})

    def get_absolute_url(self):
        return reverse('project:detail', kwargs={'slug': self.slug})
