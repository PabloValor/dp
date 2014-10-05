from django.db import models
from games.models import Player

class Contact(models.Model):
    player = models.ForeignKey(Player)
    text = models.TextField()
    subject = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.subject
