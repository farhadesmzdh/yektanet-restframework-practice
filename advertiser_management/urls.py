from django.urls import path
from .views import AdClickView, AdsApiView, ClickCountApiView, RatioClickByApiView, TimeBetweenClickApiView


urlpatterns = [
    path('api/ads/', AdsApiView.as_view(), name='ads_view'),
    path('api/ad_click/<int:ad_id>/', AdClickView.as_view(), name='ad_click'),
    path('api/add_ad/', AdsApiView.as_view(), name='add_ad'),
    path('api/click_count/', ClickCountApiView.as_view(), name='click_count'),
    path('api/ratio_click_view/', RatioClickByApiView.as_view(), name='ratio_click_view'),
    path('api/time_between_click_view/', TimeBetweenClickApiView.as_view(), name='time_between_click_view'),
]


