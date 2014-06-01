from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from tournaments.models import Tournament, Team, Fixture, Match

class Player(User):
    initial_points = models.IntegerField(verbose_name = 'Puntos iniciales', default = 0)

    def __unicode__(self):
        return self.username

    def make_prediction(self, match_id, local_team_goals, visitor_team_goals):
        prediction = PlayerMatchPrediction.objects.filter(match_id = match_id, player_id = self.pk)
        if prediction:
            prediction.update(local_team_goals = local_team_goals,
                              visitor_team_goals = visitor_team_goals)
        else:
            PlayerMatchPrediction.objects.create(player = self,
                                        match_id = match_id, 
                                        local_team_goals = local_team_goals, 
                                        visitor_team_goals = visitor_team_goals)

    def get_total_points(self, game):
        return FixturePlayerPoints.get_player_points(game.id, self.id) + self.initial_points

    def get_fixture_points(self, fixture, game):
        points = 0
        if fixture.is_finished:
            points = sum([player_prediction.get_points(game) 
                        for player_prediction in self.playermatchprediction_set.all() 
                        if not player_prediction.match.suspended and player_prediction.match.fixture.pk == fixture.pk])
    
        return points + self.initial_points

    def get_fixture_predictions(self, fixture):
        match_ids = [x.pk for x in fixture.match_set.all()]
        predictions = self.playermatchprediction_set.filter(match_id__in = match_ids)

        return predictions
        
    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"

class Game(models.Model):
    owner = models.ForeignKey(Player, related_name = 'owner_games')
    players =  models.ManyToManyField(Player, related_name = 'games')
    name = models.CharField(max_length = 100)
    tournament = models.ForeignKey(Tournament)
    classic = models.BooleanField(default = True, verbose_name = "Modo Clasico")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Juego"


class PlayerMatchPrediction(models.Model):
    player = models.ForeignKey(Player)
    match = models.ForeignKey(Match)
    local_team_goals = models.PositiveIntegerField()
    visitor_team_goals = models.PositiveIntegerField()
    is_double = models.BooleanField(verbose_name = "Doble", default = False)

    def is_a_moral_prediction(self):
        prediction_local_team_had_won = self.__class__.has_local_team_won(self.local_team_goals, self.visitor_team_goals)
        match_local_team_had_won = self.__class__.has_local_team_won(self.match.local_team_goals, self.match.visitor_team_goals)

        return prediction_local_team_had_won == match_local_team_had_won

    def is_a_exact_prediction(self):
        return self.match.local_team_goals == self.local_team_goals and  \
               self.match.visitor_team_goals == self.visitor_team_goals

    def get_points(self, game):
        if game.classic:
            return self.get_points_classic()
        else:
            return self.get_points_dp()

    def get_points_classic(self):
        if self.is_a_moral_prediction():
            return 1
        else:
            return 0

    def get_points_dp(self):
        points = 0
        if self.is_a_exact_prediction():
            points = settings.POINTS['exact']
        elif self.is_a_moral_prediction():
            points = settings.POINTS['moral']

        if self.match.is_classic:
            points *= settings.POINTS['classic']

        if self.is_double:
            points *= settings.POINTS['double']

        return points

    @classmethod
    def has_local_team_won(cls, local_team_goals, visitor_team_goals):
    # None = draw, True = won, False = lose
        return None if visitor_team_goals == local_team_goals else (visitor_team_goals < local_team_goals)

class FixturePlayerPoints(models.Model):
    fixture = models.ForeignKey(Fixture)
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game) # For simplest queries 
    points = models.IntegerField(verbose_name = 'Puntos')

    def __unicode__(self):
        return "{0} - {1} = {2} puntos".format(self.player, self.fixture, self.points)

    @classmethod
    def get_player_points(cls, game_id, player_id):
        fixtures_points = [x.points for x in cls.objects.filter(game_id = game_id, player_id = player_id)]
        return sum(fixtures_points)

    class Meta:
        verbose_name = "Fecha punto"

