from itertools import chain

from django.db.models import Count, Avg, F, When, Case, Value, FloatField
from django.db.models.functions import TruncHour
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.generic import RedirectView
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Ad, Click, Views
from .serializers import AdSerializer, ClickCountSerializer, RatioClickByViewSerializer, TimeBetweenClickSerializer


class AdsApiView(generics.ListCreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdClickView(RedirectView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, id=kwargs['ad_id'])
        return ad.link


class ClickCountApiView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ClickCountSerializer

    def get(self, request, *args, **kwargs):
        total_clicks = Click.objects.count()

        clicks_per_ad = (
            Click.objects
            .values('ad_id')
            .annotate(count=Count('id'))
        )

        clicks_per_hour = (
            Click.objects
            .annotate(hour=TruncHour('time'))
            .values('ad_id', 'hour')
            .annotate(count=Count('id'))
        )

        data = {
            'total_clicks': total_clicks,
            'clicks_per_ad': list(clicks_per_ad),
            'clicks_per_hour': list(clicks_per_hour),
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid()

        return Response(serializer.data)


class RatioClickByApiView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RatioClickByViewSerializer

    def get(self, request, *args, **kwargs):
        count_click = Click.objects.annotate(hour=TruncHour('time')).values('hour').annotate(
            click_count=Count('id')).values('hour', 'click_count')
        count_view = Views.objects.annotate(hour=TruncHour('time')).values('hour').annotate(
            view_count=Count('id')).values('hour', 'view_count')

        # Perform left outer join
        merged_data = count_view.annotate(click_count=Case(
            When(hour=F('hour'), then=F('view_count')),
            default=Value(0),
            output_field=FloatField()
        )).values('hour', 'view_count', 'click_count')

        # Calculate the ratio
        context = merged_data.annotate(ratio=Case(
            When(view_count=0, then=Value(0)),
            default=F('click_count') / F('view_count'),
            output_field=FloatField()
        ))

        serialized_result = RatioClickByViewSerializer(context, many=True).data

        return Response(serialized_result)


class TimeBetweenClickApiView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TimeBetweenClickSerializer

    def get(self, request, *args, **kwargs):
        context = Click.objects.annotate(diff=(F('time') - F('view_id__time'))).values('ad_id').annotate(
            average=Avg('diff'))

        for entry in context:
            entry['average'] = entry['average'].total_seconds()
        print(context)

        serialized_result = self.serializer_class(context, many=True).data
        return Response(serialized_result)
