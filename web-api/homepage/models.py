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

