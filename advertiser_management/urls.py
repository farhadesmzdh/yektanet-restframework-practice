from django.urls import path
from .views import AdClickView, AdsApiView, ClickCountApiView, RatioClickByApiView, TimeBetweenClickApiView


urlpatterns = [
    path('ads/', AdsApiView.as_view(), name='ads_view'),
    path('ad_click/<int:ad_id>/', AdClickView.as_view(), name='ad_click'),
    path('add_ad/', AdsApiView.as_view(), name='add_ad'),
    path('click_count/', ClickCountApiView.as_view(), name='click_count'),
    path('ratio_click_view/', RatioClickByApiView.as_view(), name='ratio_click_view'),
    path('time_between_click_view/', TimeBetweenClickApiView.as_view(), name='time_between_click_view'),
]


