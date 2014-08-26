from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from tournaments.models import Tournament, Team, Fixture, Match

class Player(AbstractUser):
    REQUIRED_FIELDS = ["email", ]

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

    def is_friend(self, player):
        return player in self.get_true_friends()

    def make_prediction(self, gameplayer_id, match_id, local_team_goals, visitor_team_goals):
        prediction = PlayerMatchPrediction.objects.filter(match_id = match_id, gameplayer_id = gameplayer_id)
        if prediction:
            prediction.update(local_team_goals = local_team_goals,
                              visitor_team_goals = visitor_team_goals)
        else:
            PlayerMatchPrediction.objects.create(gameplayer_id = gameplayer_id,
                                        match_id = match_id, 
                                        local_team_goals = local_team_goals, 
                                        visitor_team_goals = visitor_team_goals)

    def get_total_points(self, game):
        gameplayer = self.get_gameplayer(game)
        return FixturePlayerPoints.get_player_points(gameplayer) + gameplayer.initial_points

    def get_gameplayer(self, game):
        return self.gameplayer_set.get(game = game, status = True)

    def get_fixture_points(self, fixture, game):
        gameplayer = self.get_gameplayer(game)

        points = 0
        if fixture.is_finished:
            points = sum([player_prediction.get_points() 
                        for player_prediction in gameplayer.match_predictions.all() 
                        if not player_prediction.match.suspended and player_prediction.match.fixture.pk == fixture.pk and player_prediction.match.is_finished])
    
        return points + gameplayer.initial_points

    def get_fixture_predictions(self, fixture, game):
        gameplayer = self.get_gameplayer(game)

        match_ids = [x.pk for x in fixture.matches.all()]
        predictions = gameplayer.match_predictions.filter(match_id__in = match_ids)

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
    open_predictions = models.BooleanField(default = True, verbose_name = "Pronosticos Abiertos")

    points_exact = models.PositiveIntegerField(default = 3)
    points_general = models.PositiveIntegerField(default = 3)
    points_classic = models.PositiveIntegerField(default = 2)
    points_double = models.PositiveIntegerField(default = 2)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Juego"

class GamePlayer(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL)
    game = models.ForeignKey(Game)
    status = models.NullBooleanField()
    another_chance = models.NullBooleanField()
    initial_points = models.PositiveIntegerField(default = 0)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
      return '{0} | {1} | {2}'.format(self.player, self.status, self.another_chance)

class PlayerMatchPrediction(models.Model):
    gameplayer = models.ForeignKey(GamePlayer, related_name = 'match_predictions')
    match = models.ForeignKey(Match)
    local_team_goals = models.PositiveIntegerField()
    visitor_team_goals = models.PositiveIntegerField()
    is_double = models.BooleanField(verbose_name = "Doble", default = False)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def game(self):
      return self.gameplayer.game

    def is_general_prediction(self):
        prediction_local_team_had_won = self.__class__.has_local_team_won(self.local_team_goals, self.visitor_team_goals)
        match_local_team_had_won = self.__class__.has_local_team_won(self.match.local_team_goals, self.match.visitor_team_goals)

        return prediction_local_team_had_won == match_local_team_had_won

    def is_a_exact_prediction(self):
        return self.match.local_team_goals == self.local_team_goals and  \
               self.match.visitor_team_goals == self.visitor_team_goals

    def get_points(self):
        if not self.match.is_finished:
          return None

        points = 0

        # General Prediction: Who won or if they draw 
        if self.is_general_prediction():
            points += self.gameplayer.game.points_general

        # Exact Prediction: The exact score of the match
        if (not self.gameplayer.game.classic) and self.is_a_exact_prediction():
            points += self.gameplayer.game.points_exact

        # If the match is classic
        # Only sums if the player predicted correctly a General or Exact Prediction
        if self.match.is_classic and points > 0:
            points += self.gameplayer.game.points_classic

        # If the match is double
        # Only multiplies if the player predicted correctly a General or Exact Prediction
        if self.is_double and points > 0:
              points *= self.gameplayer.game.points_double

        return points


    @classmethod
    def has_local_team_won(cls, local_team_goals, visitor_team_goals):
    # None = draw, True = won, False = lose
        return None if visitor_team_goals == local_team_goals else (visitor_team_goals < local_team_goals)

class FixturePlayerPoints(models.Model):
    fixture = models.ForeignKey(Fixture)
    gameplayer = models.ForeignKey(GamePlayer)
    points = models.IntegerField(verbose_name = 'Puntos')

    def __unicode__(self):
        return "{0} - {1} = {2} puntos".format(self.gameplayer.player, self.fixture, self.points)

    @classmethod
    def get_player_points(cls, gameplayer):
        fixtures_points = [x.points for x in cls.objects.filter(gameplayer = gameplayer)]
        return sum(fixtures_points)

    class Meta:
        verbose_name = "Fecha punto"

