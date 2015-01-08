# -*- encoding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError
from tournaments.models import Tournament

class TournamentHomepage(models.Model):
    tournament = models.ForeignKey(Tournament)

    def __unicode__(self):
        return self.tournament.name

    def clean(self):
        if TournamentHomepage.objects.filter(tournament = self.tournament).exists():
            raise ValidationError('Repeated Tournament. Already saved.')

class News(models.Model):
    title = models.TextField()
    description = models.TextField()
    link = models.TextField(blank = True, null = True)
    active = models.BooleanField(default = False)
    date = models.DateField(auto_now_add = True)

    def __unicode__(self):
        return u"{0} {1}".format(self.date, self.title)

    class Meta:
        verbose_name_plural = "News"    
