from rest_framework import serializers
from .models import Advertiser, Ad


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class ClickCountSerializer(serializers.Serializer):
    total_clicks = serializers.IntegerField()
    clicks_per_ad = serializers.ListField(child=serializers.DictField())
    clicks_per_hour = serializers.ListField(child=serializers.DictField())


class RatioClickByViewSerializer(serializers.Serializer):
    ad_id = serializers.IntegerField()
    hour = serializers.DateTimeField()
    count_click = serializers.IntegerField()
    count_view = serializers.IntegerField()
    ratio = serializers.FloatField()


class TimeBetweenClickSerializer(serializers.Serializer):
    ad_id = serializers.IntegerField()
    avg_seconds = serializers.FloatField()
