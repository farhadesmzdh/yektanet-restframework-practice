from django.db.models import Count, Avg, F
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
        result_click = (
            Click.objects
            .annotate(hour=TruncHour('time'))
            .values('ad_id', 'hour')
            .annotate(count_click=Count('ad_id'))
            .order_by('-hour', '-count_click')
        )

        result_view = (
            Views.objects
            .annotate(hour=TruncHour('time'))
            .values('ad_id', 'hour')
            .annotate(count_view=Count('ad_id'))
            .order_by('-hour', '-count_view')
        )

        result = []
        total_ratio = 0

        for click_entry in result_click:
            ad_id = click_entry['ad_id']
            hour = click_entry['hour']
            count_click = click_entry['count_click']

            view_entry = next(
                (entry for entry in result_view if entry['ad_id'] == ad_id and entry['hour'] == hour),
                None
            )
            count_view = view_entry['count_view'] if view_entry else 0

            ratio = count_click / count_view if count_view != 0 else None

            total_ratio += ratio if ratio is not None else 0

            result.append({
                'ad_id': ad_id,
                'hour': hour,
                'count_click': count_click,
                'count_view': count_view,
                'ratio': ratio
            })

        result = sorted(result, key=lambda x: x['ratio'], reverse=True)
        total_ratio /= len(result) if result else 1

        serialized_result = self.serializer_class(result, many=True).data
        context = {'result': serialized_result, 'total_ratio': total_ratio}
        return Response(context)


class TimeBetweenClickApiView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TimeBetweenClickSerializer

    def get(self, request, *args, **kwargs):
        average_timedelta_per_ad = Click.objects.values('ad_id').annotate(
            avg_time_diff=Avg(F('time') - F('view_id__time'))
        )

        for entry in average_timedelta_per_ad:
            entry['avg_seconds'] = entry['avg_time_diff'].total_seconds()

        serialized_result = self.serializer_class(average_timedelta_per_ad, many=True).data
        return Response(serialized_result)


