from django.urls import path
from .views import AdsView, AdClickView, AddAdView, ClickCountView, RatioClickByView, TimeBetweenClickView

urlpatterns = [
    path('ads/', AdsView.as_view(), name='ads_view'),
    path('ad_click/<int:ad_id>/', AdClickView.as_view(), name='ad_click'),
    path('add_ad/', AddAdView.as_view(), name='add_ad'),
    path('click_count/', ClickCountView.as_view(), name='click_count'),
    path('ratio_click_view/', RatioClickByView.as_view(), name='ratio_click_view'),
    path('time_between_click_view/', TimeBetweenClickView.as_view(), name='time_between_click_view'),
]
