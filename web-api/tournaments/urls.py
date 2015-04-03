from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = patterns('tournaments.views',
                    url(r'^$', TournamentList.as_view(), name = 'tournamentList'),
                    url(r'^teams$', TournamentTeamsList.as_view(), name = 'tournamentTeamsList'),                       
                    url(r'^fixtures/next$', AllTournamentNextFixtureList.as_view(), name = 'allTournamentNextFixtureList'),
                    url(r'^fixtures/current-or-last$', AllTournamentCurrentOrLastFixtureList.as_view(), name = 'allTournamentCurrentOrLastFixtureList'),                       
                    url(r'^fixtures/(?P<pk>[0-9]+)$', TournamentFixture.as_view(), name = 'tournamentFixture'),
                    url(r'^(?P<pk>[0-9]+)/fixture$', TournamentAllFixtures.as_view(), name = 'tournamentAllFixtures'),
                    url(r'^(?P<pk>[0-9]+)/stats$', TournamentStats.as_view(), name = 'tournamentStats'),                       
)

urlpatterns = format_suffix_patterns(urlpatterns)
