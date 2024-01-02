from django.db import models


class Advertiser(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False)
    name = models.CharField(null=False, max_length=256)
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)


class Ad(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False)
    title = models.CharField(max_length=256, null=False)
    imgUrl = models.URLField(max_length=256)
    link = models.URLField(max_length=256)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    approve = models.BooleanField(default=False, blank=True)


class Views(models.Model):
    ad_id = models.ForeignKey(Ad, on_delete=models.CASCADE, to_field="id")
    time = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)


class Click(models.Model):
    ad_id = models.ForeignKey(Ad, on_delete=models.CASCADE, to_field="id")
    time = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    view_id = models.ForeignKey(Views, on_delete=models.CASCADE)




