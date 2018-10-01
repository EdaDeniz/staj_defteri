from __future__ import unicode_literals

import uuid

from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = RichTextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)
    slug = models.UUIDField(default=uuid.uuid4)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_delete_url(self):
        return reverse('post:delete', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post:update', kwargs={'slug': self.slug})

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    # post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)

    name = models.CharField(max_length=200, verbose_name='name')
    content = models.TextField(verbose_name='comment')
    # tarih bilgisini otomatik doldurma
    created_date = models.DateTimeField(auto_now_add=True)
