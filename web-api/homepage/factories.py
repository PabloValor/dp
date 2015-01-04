import factory
from .models import TournamentHomepage
from tournaments.factories import TournamentFactory

class TournamentHomepageFactory(factory.Factory):
    tournament = factory.LazyAttribute(lambda a: TournamentFactory())
