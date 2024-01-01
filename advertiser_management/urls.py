from django.urls import path
from .views import ads_view, ad_click, add_ad

urlpatterns = [
    path('ads/', ads_view, name='ads_view'),
    path('ad_click/<int:ad_id>/', ad_click, name='ad_click'),
    path('add_ad/', add_ad, name='add_ad'),
]
