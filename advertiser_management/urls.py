# advertiser_management/urls.py

from django.urls import path
from .views import ads_view

urlpatterns = [
    path('ads/', ads_view, name='ads_view'),
]
