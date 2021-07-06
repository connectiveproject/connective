from rest_framework import serializers

from ..models import School


class SchoolSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    last_updated_by = serializers.CharField(
        source="last_updated_by.slug",
        read_only=True,
    )

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
            "last_updated_by",
        ]

    extra_kwargs = {"url": {"view_name": "api:school-detail", "lookup_field": "slug"}}
