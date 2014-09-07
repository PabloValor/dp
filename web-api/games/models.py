from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from tournaments.models import Tournament, Team, Fixture, Match

class Player(AbstractUser):
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

    def reset(self):
        self.status = None
        self.another_chance = None

    def is_invited(self):
        """ Was invited to play """
        return self.status == None and self.another_chance == None

    def is_answered_request(self):
        """ Answered the request to play """
        return (not self.status == None) and self.another_chance == None

    def is_another_chance(self):
        """ Asks for antother invitation """
        return self.another_chance and self.status == False

    def get_total_points(self):
        return FixturePlayerPoints.get_player_points(self) + self.initial_points

    def get_fixture_points(self, fixture):
        points = self.initial_points
        classic = False

        if fixture.is_finished:
          predictions = self.match_predictions.filter(match__fixture = fixture, match__is_finished = True)
          for player_prediction in predictions:
            prediction_points = player_prediction.get_points()

            if prediction_points > 0 and player_prediction.match.is_classic:
              classic = True

            points = prediction_points + points

        return (points , classic)

    def get_fixture_predictions(self, fixture):
        match_ids = [x.pk for x in fixture.matches.all()]
        predictions = self.match_predictions.filter(match_id__in = match_ids)

        return predictions

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

    def is_general_prediction(self):
        if not self.match.is_finished:
            return False

        prediction_local_team_had_won = self.__class__.has_local_team_won(self.local_team_goals, self.visitor_team_goals)
        match_local_team_had_won = self.__class__.has_local_team_won(self.match.local_team_goals, self.match.visitor_team_goals)

        return prediction_local_team_had_won == match_local_team_had_won

    def is_exact_prediction(self):
        if not self.match.is_finished:
            return False

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
        if (not self.gameplayer.game.classic) and self.is_exact_prediction():
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
    classic_prediction = models.BooleanField(default = False)

    def __unicode__(self):
        return "{0} - {1} = {2} puntos".format(self.gameplayer.player, self.fixture, self.points)

    @classmethod
    def get_player_points(cls, gameplayer):
        fixtures_points = [x.points for x in cls.objects.filter(gameplayer = gameplayer)]
        return sum(fixtures_points)

    class Meta:
        verbose_name = "Fecha punto"

