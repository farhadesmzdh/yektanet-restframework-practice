from django.shortcuts import render, redirect, get_object_or_404
from .models import Advertiser, Ad
from .forms import AdForm


def ads_view(request):
    advertisers = Advertiser.objects.all()
    ads_grouped = {advertiser: Ad.objects.filter(advertiser=advertiser) for advertiser in advertisers}

    return render(request, 'ads_view.html', {'grouped_ads': ads_grouped})


def ad_click(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    ad.incClicks()
    return redirect(ad.link)


def add_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            advertiser_id = form.cleaned_data['advertiserID']

            advertiser = get_object_or_404(Advertiser, pk=advertiser_id)

            ad = form.save(commit=False)
            ad.advertiser = advertiser
            ad.save()

            return redirect('ads_view')
    else:
        form = AdForm()

    return render(request, 'ad_form.html', {'form': form})


