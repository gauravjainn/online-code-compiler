from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User


class TimeStamp(models.Model):

    """An Abstract class which takes care of these 2 time stamp fields in child classes"""

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CodeUrl(TimeStamp):

    """Latest/Current language and code for a particular URI"""

    LANGUAGE_CHOICES = (
        ('C', 'C'),
        ('CPP', 'C++'),
        ('JAVA', 'Java'),
        ('PYTHON', 'Python')
    )

    uri = models.CharField(max_length=63, unique=True)
    lang = models.CharField(max_length=15, choices=LANGUAGE_CHOICES, blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.uri


class CodeHistory(TimeStamp):

    """Create logs for code history related to a URI"""

    uri = models.CharField(max_length=63)
    lang = models.CharField(max_length=15, blank=True, null=True)
    code = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Code History"

    def __unicode__(self):
        return self.uri
