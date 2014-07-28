import factory
from random import randrange
from .models import Player, PlayerMatchPrediction, Game, FixturePlayerPoints, GamePlayer
from tournaments.factories import *

class GameFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'Torneo {0}'.format(n))
    tournament = factory.LazyAttribute(lambda a: TournamentFactory())
    classic = False
    owner = factory.LazyAttribute(lambda a: PlayerFactory())

class GamePlayerFactory(factory.Factory):
    player = factory.LazyAttribute(lambda a: PlayerFactory())
    game = factory.LazyAttribute(lambda a: GameFactory())
    player_invitation_status = False

class PlayerFactory(factory.Factory):
    username = factory.Sequence(lambda n: 'name_{0}'.format(n))
    password = factory.Sequence(lambda n: 'password_{0}'.format(n))

class PlayerMatchPredictionFactory(factory.Factory):
    player = factory.LazyAttribute(lambda a: PlayerFactory())
    match = factory.LazyAttribute(lambda a: MatchFactory())
    local_team_goals = randrange(0, 5)
    visitor_team_goals = randrange(0, 5)
    is_double = False

class FixturePlayerPointsFactory(factory.Factory):
    fixture = factory.LazyAttribute(lambda a: FixtureFactory())
    player = factory.LazyAttribute(lambda a: PlayerFactory())
    game = factory.LazyAttribute(lambda a: GameFactory())
    points = randrange(0, 5)


