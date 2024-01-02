from django.db.models import Count, Avg, F
from django.db.models.functions import TruncHour
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import RedirectView


from .models import Ad, Advertiser, Click, Views
from .forms import AdForm


class AdsView(View):
    template_name = 'ads_view.html'

    def get(self, request, *args, **kwargs):
        advertisers = Advertiser.objects.all()
        ads_grouped = {advertiser: Ad.objects.filter(advertiser=advertiser) for advertiser in advertisers}
        return render(request, self.template_name, {'grouped_ads': ads_grouped})


class AdClickView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, id=kwargs['ad_id'])
        return ad.link


class AddAdView(View):
    template_name = 'ad_form.html'

    def get(self, request, *args, **kwargs):
        form = AdForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AdForm(request.POST)
        if form.is_valid():
            advertiser_id = form.cleaned_data['advertiserID']
            advertiser = get_object_or_404(Advertiser, pk=advertiser_id)

            ad = form.save(commit=False)
            ad.advertiser = advertiser
            ad.save()

            return redirect('ads_view')

        return render(request, self.template_name, {'form': form})


class ClickCountView(View):
    template_name = 'click_count.html'

    def get_context_data(self, **kwargs):
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

        context = {'total_clicks': total_clicks, 'clicks_per_ad': clicks_per_ad, 'clicks_per_hour': clicks_per_hour}
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class RatioClickByView(View):
    template_name = 'ratio_click_view.html'

    def get_context_data(self, **kwargs):
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

        context = {'result': result, 'total_ratio': total_ratio}
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class TimeBetweenClickView(View):
    template_name = 'time_between_click_view.html'

    def get_context_data(self, **kwargs):
        average_timedelta_per_ad = Click.objects.values('ad_id').annotate(
            avg_time_diff=Avg(F('time') - F('view_id__time'))
        )

        for entry in average_timedelta_per_ad:
            entry['avg_seconds'] = entry['avg_time_diff'].total_seconds()
        return {'average_per_ad': average_timedelta_per_ad}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

