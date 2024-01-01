from django.urls import path
from .views import AdsView, AdClickView, AddAdView

urlpatterns = [
    path('ads/', AdsView.as_view(), name='ads_view'),
    path('ad_click/<int:ad_id>/', AdClickView.as_view(), name='ad_click'),
    path('add_ad/', AddAdView.as_view(), name='add_ad'),
]
