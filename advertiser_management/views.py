from django.shortcuts import render
from .models import Advertiser, Ad


def ads_view(request):
    advertisers = Advertiser.objects.all()
    ads_grouped = {advertiser: Ad.objects.filter(advertiser=advertiser) for advertiser in advertisers}

    return render(request, 'ads_view.html', {'grouped_ads': ads_grouped})
