from rest_framework import serializers
from .models import Urls

class UrlsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Urls
        fields = ('id', 'url', 'short_url', 'text_message', 'click_count', 'add_date')
