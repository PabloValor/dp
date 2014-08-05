from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from tournaments.models import Tournament, Team, Fixture, Match

class Player(AbstractUser):
    REQUIRED_FIELDS = ["email", ]

    initial_points = models.IntegerField(verbose_name = 'Puntos iniciales', default = 0)
    friends = models.ManyToManyField('self', through = 'PlayerFriend', symmetrical = False)

    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"

    def __unicode__(self):
        return self.username

    # Think other way to do this
    # < --
    def get_all_friends(self):
        players = [pf.player for pf in self.friend.filter()]
        friends = [pf.friend for pf in self.friend_player.filter()]
        return players + friends

    def get_true_friends(self):
        players = [pf.player for pf in self.friend.filter(status = True)]
        friends = [pf.friend for pf in self.friend_player.filter(status = True)]
        return players + friends

    def get_ignored_friends(self):
        # Friends that ask you to be your friend but you didn't answer the Friends Petition
        friends = [pf.player for pf in self.friend.filter(status = None)]
        return friends

    def get_friends_that_ignored_us(self):
        friends = [pf.friend for pf in self.friend_player.filter(status = None)]
        return friends

    def get_bad_friends(self):
        friends = [pf.friend for pf in self.friend_player.filter(status = False)]
        return friends

    def get_friends_we_rejected(self):
        friends = [pf.player for pf in self.friend.filter(status = False)]
        return friends
    # -- >

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

class PlayerFriend(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'friend_player')
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'friend')
    status = models.NullBooleanField()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
      return '{0} - {1}'.format(self.player, self.friend)


class Game(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'owner_games')
    players =  models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'games',through = 'GamePlayer')
    name = models.CharField(max_length = 100)
    tournament = models.ForeignKey(Tournament)
    classic = models.BooleanField(default = True, verbose_name = "Modo Clasico")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Juego"

class GamePlayer(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL)
    game = models.ForeignKey(Game)
    player_invitation_status = models.NullBooleanField()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class PlayerMatchPrediction(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL)
    match = models.ForeignKey(Match)
    local_team_goals = models.PositiveIntegerField()
    visitor_team_goals = models.PositiveIntegerField()
    is_double = models.BooleanField(verbose_name = "Doble", default = False)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

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
    player = models.ForeignKey(settings.AUTH_USER_MODEL)
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

