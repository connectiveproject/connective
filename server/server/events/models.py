from django.db import models

from server.organizations.models import SchoolActivityGroup
from server.users.models import Consumer


class Event(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    consumers = models.ManyToManyField(Consumer)
    school_group = models.ForeignKey(
        SchoolActivityGroup, on_delete=models.SET_NULL, null=True, blank=True
    )
    locations_name = models.CharField(max_length=250, null=True, blank=True)
