from celery import shared_task
from django.db.models import Count
from .models import Ad, Click, Views
from django.utils import timezone
from .models import ViewCount, ClickCount

@shared_task
def ClicksInPastHour():
    current_time = timezone.now()
    past_hour = current_time - timezone.timedelta(hours=1)
    clicks_with_counts = Click.objects.filter(time__range=(past_hour, current_time)).values('ad_id').annotate(count=Count('time'))
    hourly_click_counts = []
    for click_data in clicks_with_counts:
        ad_id = click_data['ad_id']
        ad = Ad.objects.get(id=ad_id)
        count = click_data['count']
        hourly_click_count_instance = ClickCount(
            from_time=past_hour,
            to_time=current_time,
            ad_id=ad,
            count=count
        )
        hourly_click_counts.append(hourly_click_count_instance)

    print(hourly_click_counts)

    ClickCount.objects.bulk_create(hourly_click_counts)

@shared_task
def ClicksInPastDay():
    current_time = timezone.now()
    past_day = current_time - timezone.timedelta(days=1)
    clicks_with_counts = Click.objects.filter(time__range=(past_day, current_time)).values('ad_id').annotate(
        count=Count('time'))
    daily_click_counts = []
    for click_data in clicks_with_counts:
        ad_id = click_data['ad_id']
        ad = Ad.objects.get(id=ad_id)
        count = click_data['count']
        daily_click_count_instance = ClickCount(
            from_time=past_day,
            to_time=current_time,
            ad_id=ad,
            count=count
        )
        daily_click_counts.append(daily_click_count_instance)

    print(daily_click_counts)

    ClickCount.objects.bulk_create(daily_click_counts)

@shared_task
def ViewsInPastHour():
    current_time = timezone.now()
    past_hour = current_time - timezone.timedelta(hours=1)
    views_with_counts = Views.objects.filter(time__range=(past_hour, current_time)).values('ad_id').annotate(count=Count('time'))
    hourly_view_counts = []
    for view_data in views_with_counts:
        ad_id = view_data['ad_id']
        ad = Ad.objects.get(id=ad_id)
        count = view_data['count']

        hourly_view_count_instance = ViewCount(
            from_time=past_hour,
            to_time=current_time,
            ad_id=ad,
            count=count
        )

        hourly_view_counts.append(hourly_view_count_instance)

        for instance in hourly_view_counts:
            instance.id = None

        ViewCount.objects.bulk_create(hourly_view_counts)


@shared_task
def ViewsInPastDay():
    current_time = timezone.now()
    past_day = current_time - timezone.timedelta(days=1)
    views_with_counts = Views.objects.filter(time__range=(past_day, current_time)).values('ad_id').annotate(
        count=Count('time'))
    daily_view_counts = []
    for view_data in views_with_counts:
        ad_id = view_data['ad_id']
        ad = Ad.objects.get(id=ad_id)
        count = view_data['count']

        daily_view_count_instance = ViewCount(
            from_time=past_day,
            to_time=current_time,
            ad_id=ad,
            count=count
        )

        daily_view_counts.append(daily_view_count_instance)

        for instance in daily_view_counts:
            instance.id = None

        ViewCount.objects.bulk_create(daily_view_counts)