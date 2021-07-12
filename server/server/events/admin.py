from django.contrib import admin

from .models import Event

admin.site.register(Event)

def get_covid_stats(country):
    "gets infection rate for country"
    