from rest_framework import serializers
from api.models import AvgEvents, UrlsMetric, Events

class EventHoursSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    class Meta:
        model = AvgEvents
        fields = ['hour', 'count']

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlsMetric
        fields = ['url', 'pageBeforeConversion', 'pageBeforeShare', 'total_clicks', 'unique_clicks', 'timeonpage_filtered']

class EventTypesSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    person__locale = serializers.CharField()
    class Meta:
        model = Events
        fields = ['person__locale', 'count']