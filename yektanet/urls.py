from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('advertiser_management/', include('advertiser_management.urls')),
]
