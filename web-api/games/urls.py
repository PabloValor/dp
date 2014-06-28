from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GameList, GameDetail, PlayerList, PlayerDetail, PlayerCreate, PlayerUpdate

urlpatterns = patterns('games.views',
        url(r'^$', GameList.as_view(), name = 'gameList'),
        url(r'^(?P<pk>[0-9]+)/$', GameDetail.as_view(), name = 'gameDetail'),
        url(r'^player/$', PlayerCreate.as_view(), name = 'playerCreate'),
        url(r'^player/(?P<pk>[0-9]+)/$', PlayerUpdate.as_view(), name = 'playerUpdate'),
        url(r'^players/$', PlayerList.as_view(), name = 'playerList'),
        url(r'^players/(?P<pk>[0-9]+)/$', PlayerDetail.as_view(), name = 'playerDetail'),
        url(r'^sociallogin/', 'social_register'),
)


urlpatterns = format_suffix_patterns(urlpatterns)
