from rest_framework import serializers

from ..models import School


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = School
        fields = [
            "slug",
            "name",
            "address",
            "address_city",
            "zip_city",
            "school_code",
            "description",
            "contact_phone",
            "website",
            "profile_picture",
            "grade_levels",
        ]

    extra_kwargs = {"url": {"view_name": "api:school-detail", "lookup_field": "slug"}}
