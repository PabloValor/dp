import factory
from datetime import datetime, timedelta
from random import randrange
from .models import Player, PlayerMatchPrediction, Game, FixturePlayerPoints
from tournaments.models import  Team, Fixture, Match, Tournament

class TournamentFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'Torneo {0}'.format(n))

class GameFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'Torneo {0}'.format(n))
    tournament = factory.LazyAttribute(lambda a: TournamentFactory())
    classic = False

class TeamFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'Team {0}'.format(n))

class FixtureFactory(factory.Factory):
    is_finished = False
    number = randrange(0, 20)
    tournament = factory.LazyAttribute(lambda a: TournamentFactory())
    open_until = datetime.now()

class MatchFactory(factory.Factory):
    date = datetime.now()
    local_team = factory.LazyAttribute(lambda a: TeamFactory())
    visitor_team = factory.LazyAttribute(lambda a: TeamFactory())
    fixture = factory.LazyAttribute(lambda a: FixtureFactory())
    suspended = False
    local_team_goals = randrange(0, 5)
    visitor_team_goals = randrange(0, 5)
    is_classic = False

class PlayerFactory(factory.Factory):
    username = factory.Sequence(lambda n: 'Name {0}'.format(n))
    game = factory.LazyAttribute(lambda a: GameFactory())

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


