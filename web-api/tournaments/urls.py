from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (TournamentList, TournamentFixture, AllTournamentNextFixtureList,
                    AllTournamentCurrentOrLastFixtureList, TournamentStats)

urlpatterns = patterns('tournaments.views',
                    url(r'^$', TournamentList.as_view(), name = 'tournamentList'),
                    url(r'^fixtures/next$', AllTournamentNextFixtureList.as_view(), name = 'allTournamentNextFixtureList'),
                    url(r'^fixtures/current-or-last$', AllTournamentCurrentOrLastFixtureList.as_view(), name = 'allTournamentCurrentOrLastFixtureList'),                       
                    url(r'^(?P<pk>[0-9]+)/fixture$', TournamentFixture.as_view(), name = 'tournamentFixture'),
                    url(r'^(?P<pk>[0-9]+)/stats$', TournamentStats.as_view(), name = 'tournamentStats'),                       
)

urlpatterns = format_suffix_patterns(urlpatterns)
