# coding: utf-8
"""
   여보세요 Models
"""
from django.db import models


class Trigger(models.Model):

    description = models.CharField(max_length=200, unique=True)
    rss_url = models.CharField(max_length=255)
    joplin_folder = models.CharField(max_length=80, null=True, blank=True)
    reddit = models.CharField(max_length=80, null=True, blank=True)
    mastodon = models.BooleanField(default=False)
    mail = models.BooleanField(default=False)
    localstorage = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_triggered = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Trigger"

    def __str__(self):
        return self.description
