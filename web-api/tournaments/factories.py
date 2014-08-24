import factory
from datetime import datetime, timedelta
from random import randrange
from .models import  Team, Fixture, Match, Tournament

class TournamentFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'Torneo {0}'.format(n))

class TeamFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'Team {0}'.format(n))

class FixtureFactory(factory.Factory):
    is_finished = False
    number = randrange(0, 20)
    tournament = factory.LazyAttribute(lambda a: TournamentFactory())
    open_until = datetime.now() + timedelta(days = 1)

class MatchFactory(factory.Factory):
    date = datetime.now().date()
    local_team = factory.LazyAttribute(lambda a: TeamFactory())
    visitor_team = factory.LazyAttribute(lambda a: TeamFactory())
    fixture = factory.LazyAttribute(lambda a: FixtureFactory())
    suspended = False
    local_team_goals = randrange(0, 5)
    visitor_team_goals = randrange(0, 5)
    is_classic = False
