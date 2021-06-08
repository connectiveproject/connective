from django.db import models

from server.users.models import Consumer

from server.organizations.models import SchoolActivityGroup

class Event(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    consumers = models.ManyToManyField(Consumer, on_delete=models.SET_NULL)
    school_group = models.ForeignKey(SchoolActivityGroup, on_delete=models.SET_NULL)
    locations_name = models.CharField(max_length=250, null=True, blank=True)
