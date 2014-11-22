from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TournamentList, TournamentFixtureList, AllTournamentCurrentFixtureList

urlpatterns = patterns('tournaments.views',
                    url(r'^$', TournamentList.as_view(), name = 'tournamentList'),
                    url(r'^/fixtures$', AllTournamentCurrentFixtureList.as_view(), name = 'allTournamentCurrentFixtureList'),
                    url(r'^(?P<pk>[0-9]+)/fixture$', TournamentFixtureList.as_view(), name = 'tournamentFixtureList'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
