from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100, blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    @property
    def rating(self):
        total_votes = Player.objects.aggregate(models.Sum('votes'))['votes__sum'] or 0
        if total_votes == 0:
            return 0
        return round((self.votes / total_votes) * 100, 2)
    
