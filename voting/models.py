from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100, blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)
    votes = models.IntegerField(default=0)
    rating = models.FloatField(default=1000.0) 
    def __str__(self):
        return self.name
