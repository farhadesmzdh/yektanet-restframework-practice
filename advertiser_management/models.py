from django.db import models


class Advertiser(models.Model):
    id = models.IntegerField(unique=True, null=False)
    name = models.CharField(null=False)
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)


class Ad(models.Manager):
    id = models.IntegerField(unique=True, null=False)
    title = models.CharField(max_length=256, null=False)
    imgUrl = models.URLField(max_length=256)
    link = models.URLField(max_length=256)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)

