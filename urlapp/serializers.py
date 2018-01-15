from rest_framework import serializers
from .models import Urls

class UrlsSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Urls
        fields = ('id', 'url', 'short_url', 'text_message', 'click_count', 'add_date')
