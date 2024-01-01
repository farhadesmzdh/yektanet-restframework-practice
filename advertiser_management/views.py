from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import RedirectView

from .models import Ad, Advertiser
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
