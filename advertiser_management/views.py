from django.shortcuts import render, redirect, get_object_or_404
from .models import Advertiser, Ad


def ads_view(request):
    advertisers = Advertiser.objects.all()
    ads_grouped = {advertiser: Ad.objects.filter(advertiser=advertiser) for advertiser in advertisers}

    return render(request, 'ads_view.html', {'grouped_ads': ads_grouped})


def ad_click(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    ad.incClicks()
    return redirect(ad.link)

