import factory
from .models import TournamentHomepage, News
from tournaments.factories import TournamentFactory

class TournamentHomepageFactory(factory.Factory):
    tournament = factory.LazyAttribute(lambda a: TournamentFactory())

class NewsFactory(factory.Factory):
    title = factory.Sequence(lambda n: 'Title {0}'.format(n))
    description = factory.Sequence(lambda n: 'Description {0}'.format(n))
    link = factory.Sequence(lambda n: 'http://www.duckduckgo.com/{0}'.format(n))
    active = True

