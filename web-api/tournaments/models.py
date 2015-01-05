from django.db import models
from django.utils import timezone

class Tournament(models.Model):
    name = models.CharField(max_length = 100)
    is_finished = models.BooleanField(default = False)

    def get_current_fixture(self):
        fixtures = self.get_future_fixtures()
        if fixtures.exists():
           return fixtures.first()
        else:
           return None

    def get_current_or_last_fixture(self):
        fixture = self.fixtures.filter(is_finished = False, is_playing = True)
        if fixture.exists():
            return fixture[0]

        last_fixture = self.get_last_fixture()
        if last_fixture.exists():
            return last_fixture[0]
        else:
            return self.get_current_fixture()

    def get_current_fixture_number(self):
        fixture = self.get_current_fixture()
        if fixture:
          return fixture.number
        else:
          return None

    def get_first_fixture(self):
        return self.fixtures.order_by('number').first()

    def get_next_fixture(self):
        fixtures = self.get_future_fixtures()
        first_fixture = self.get_first_fixture()
        
        next_fixture = None

        # If the next fixture is the first of the Tournament
        if first_fixture == fixtures.first():
            if fixtures.count() > 1:
                next_fixture =  fixtures[1]
        else:
            next_fixture = fixtures.first()               

        return next_fixture
      
    def get_past_fixtures(self):
        fixtures = self.fixtures.filter(is_finished = True).order_by('number')
        return fixtures

    def get_last_fixture(self):
        fixtures = self.fixtures.filter(is_finished = True).order_by('-number')
        return fixtures

    def get_future_fixtures(self):
      fixtures = self.fixtures.filter(is_finished = False, is_playing = False).order_by('number')
      return fixtures

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

    def get_tournament_stats(self, tournament):
        wins = 0
        draws = 0
        losses = 0
        
        for match in self.get_all_finished_matches(tournament):
            if match.get_winner() == self:
                wins += 1
            elif match.get_winner() == None:
                draws += 1
            else:
                losses += 1

        return {'w': wins, 'd': draws, 'l': losses}

    def get_all_finished_matches(self, tournament):
        return Match.get_finished(tournament, self)        
        
    class Meta:
        ordering = ['name']
        verbose_name = "Equipo"

class Fixture(models.Model):
    number = models.PositiveIntegerField(verbose_name = "Fecha numero")
    is_finished = models.BooleanField(default = False, verbose_name = "Termino")
    tournament = models.ForeignKey(Tournament, verbose_name = "Torneo", related_name = 'fixtures')
    open_until = models.DateTimeField(verbose_name = "Abierta hasta")
    is_playing  = models.BooleanField(default = False)    

    def __unicode__(self):
        return "Fecha: {0}".format(self.number)

    def get_finished_matchs(self):
        return self.match_set.filter(finished = True)

    def get_player_predictions(self, player_id):
        match_ids = [x.pk for x in self.match_set.all()]
        predictions = \
            PlayerMatchPrediction.objects.filter(player_id = player_id, match_id__in = match_ids)

        return predictions

    def is_closed(self):
      return self.open_until < timezone.now()

    class Meta:
        ordering = ['number']
        verbose_name = "Fecha"

class Match(models.Model):
    date = models.DateField(verbose_name = "Fecha", default = timezone.now().date())
    local_team = models.ForeignKey(Team, related_name = "local_team", verbose_name = "Equipo Local")
    local_team_goals = models.PositiveIntegerField(verbose_name = "Equipo Local Goles", default = 0)
    visitor_team = models.ForeignKey(Team, related_name = "visitor_team", verbose_name = "Equipo Visitante")
    visitor_team_goals = models.PositiveIntegerField(verbose_name = "Equipo Visitante Goles", default = 0)
    fixture = models.ForeignKey(Fixture, related_name = 'matches')
    suspended = models.BooleanField(verbose_name = "Suspendido", default = False)
    is_classic = models.BooleanField(verbose_name = "Clasico", default = False)
    is_finished = models.BooleanField(verbose_name = "Termino", default = False)

    def get_winner(self):
      if self.local_wins():
        return self.local_team
      elif self.visitor_wins():
        return self.visitor_team
      else:
        return None


    def local_wins(self):
        return self.local_team_goals > self.visitor_team_goals

    def visitor_wins(self):
        return self.local_team_goals < self.visitor_team_goals
 
    def nobody_wins(self):
        return self.local_team_goals == self.visitor_team_goals

    def __unicode__(self):
        return u"Fecha %s : %s vs %s " % (self.fixture.number, self.local_team.name, self.visitor_team.name)

    @classmethod
    def get_finished(cls, tournament, team):
        fixtures_ids = [fixture.id for fixture in tournament.fixtures.all()]
        matches = Match.objects.raw('select * from tournaments_match where fixture_id in %s and (local_team_id = %s or visitor_team_id = %s) and is_finished is True',
                          [tuple(fixtures_ids), team.id, team.id])
        return matches
    
    class Meta:
        verbose_name = "Partido"
