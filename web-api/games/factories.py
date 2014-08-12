import factory
from random import randrange
from .models import Player, PlayerMatchPrediction, Game, FixturePlayerPoints, GamePlayer, PlayerFriend
from tournaments.factories import *

class GameFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'Torneo {0}'.format(n))
    tournament = factory.LazyAttribute(lambda a: TournamentFactory())
    classic = False
    owner = factory.LazyAttribute(lambda a: PlayerFactory())

class GamePlayerFactory(factory.Factory):
    player = factory.LazyAttribute(lambda a: PlayerFactory())
    game = factory.LazyAttribute(lambda a: GameFactory())
    status = None
    another_chance = None

class PlayerFactory(factory.Factory):
    username = factory.Sequence(lambda n: 'name_{0}'.format(n))
    password = factory.Sequence(lambda n: 'password_{0}'.format(n))

class PlayerFriendFactory(factory.Factory):
    player = factory.LazyAttribute(lambda a: PlayerFactory())
    friend = factory.LazyAttribute(lambda a: PlayerFactory())
    status = None

class PlayerMatchPredictionFactory(factory.Factory):
    gameplayer = factory.LazyAttribute(lambda a: GamePlayerFactory())
    match = factory.LazyAttribute(lambda a: MatchFactory())
    local_team_goals = randrange(0, 5)
    visitor_team_goals = randrange(0, 5)
    is_double = False

class FixturePlayerPointsFactory(factory.Factory):
    fixture = factory.LazyAttribute(lambda a: FixtureFactory())
    gameplayer = factory.LazyAttribute(lambda a: GamePlayerFactory())
    points = randrange(0, 5)


