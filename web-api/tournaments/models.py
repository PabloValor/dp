from django.db import models
from datetime import datetime

class Tournament(models.Model):
    name = models.CharField(max_length = 100)

    def get_current_fixture(self):
        fixtures = self.fixtures.filter(is_finished = False).order_by('number')
        if fixtures.count() > 0:
           return fixtures.first()
        else:
           return None 

    def get_past_fixtures(self):
      fixtures = self.fixtures.filter(is_finished = True).order_by('number')
      return fixtures

    def get_future_fixtures(self):
      fixtures = self.fixtures.filter(is_finished = False).order_by('number')
      return fixtures

    def is_finished(self):
        return self.get_current_fixture() == None

    def get_teams(self):
      fixture = self.fixtures.first()
      teams = []
      if fixture:
        for match in fixture.matches.all():
          teams.append(match.visitor_team)
          teams.append(match.local_team)

      return teams

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Torneo"
        ordering = ['name']

class Team(models.Model):
    name = models.CharField(max_length = 50, verbose_name = "Nombre")
    crest = models.ImageField(upload_to = "crests", verbose_name = "Escudo", null = True)

    def crest_thumbnail(self):
        if self.crest:
            return '<img src="{0}" />'.format(self.crest.url)
        else:
            return ''

    crest_thumbnail.allow_tags = True

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Equipo"

class Fixture(models.Model):
    number = models.PositiveIntegerField(verbose_name = "Fecha numero")
    is_finished = models.BooleanField(default = False, verbose_name = "Termino")
    tournament = models.ForeignKey(Tournament, verbose_name = "Torneo", related_name = 'fixtures')
    open_until = models.DateTimeField(verbose_name = "Abierta hasta")

    def __unicode__(self):
        return "Fecha: {0}".format(self.number)

    def get_finished_matchs(self):
        return self.match_set.filter(finished = True)

    def get_player_predictions(self, player_id):
        match_ids = [x.pk for x in self.match_set.all()]
        predictions = \
            PlayerMatchPrediction.objects.filter(player_id = player_id, match_id__in = match_ids)

        return predictions

    def save(self, *args, **kwargs):  
        if self.is_finished:
            #FixturePlayerPoints.objects.filter(fixture = self).delete()
            self.fixtureplayerpoints = []
            for game in self.tournament.game_set.all():
                for gameplayer in game.gameplayer_set.filter(status = True):
                    points = gameplayer.player.get_fixture_points(self, game)
                    self.fixtureplayerpoints_set.create(fixture = self, gameplayer = gameplayer, points = points)
                    #FixturePlayerPoints.objects.create(fixture = self, player = player, points = points, game = game)

        super(Fixture, self).save(*args, **kwargs)

    class Meta:
        ordering = ['number']
        verbose_name = "Fecha"

class Match(models.Model):
    date = models.DateField(verbose_name = "Fecha", default = datetime.now().date())
    local_team = models.ForeignKey(Team, related_name = "local_team", verbose_name = "Equipo Local")
    local_team_goals = models.PositiveIntegerField(verbose_name = "Equipo Local Goles", default = 0)
    visitor_team = models.ForeignKey(Team, related_name = "visitor_team", verbose_name = "Equipo Visitante")
    visitor_team_goals = models.PositiveIntegerField(verbose_name = "Equipo Visitante Goles", default = 0)
    fixture = models.ForeignKey(Fixture, related_name = 'matches')
    suspended = models.BooleanField(verbose_name = "Suspendido", default = False)
    is_classic = models.BooleanField(verbose_name = "Clasico", default = False)

    def local_wins(self):
        return self.local_team_goals > self.visitor_team_goals

    def visitor_wins(self):
        return self.local_team_goals < self.visitor_team_goals

    def nobody_wins(self):
        return self.local_team_goals == self.visitor_team_goals

    def __unicode__(self):
        return u"Fecha %s : %s vs %s " % (self.fixture.number, self.local_team.name, self.visitor_team.name)

    class Meta:
        verbose_name = "Partido"
