from rest_framework import serializers

from server.schools.models import School


def school_exists(school_slug):
    if not School.objects.filter(slug=school_slug).exists():
        raise serializers.ValidationError("school_slug does not exist")
