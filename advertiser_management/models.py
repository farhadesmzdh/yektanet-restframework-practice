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
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def incClicks(self):
        self.clicks += 1
        self.save()

