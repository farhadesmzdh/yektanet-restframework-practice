from django.contrib import admin
from .models import Ad, Advertiser, Click

admin.site.register(Advertiser)
admin.site.register(Click)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'imgUrl', 'link', 'approve')
    list_filter = ('approve',)
    search_fields = ('title',)