from rest_framework import serializers

from server.connective_tags.models import ConnectiveTag


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectiveTag
        fields = ["slug", "category", "name"]
