from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = patterns('games.views',
        url(r'^$', GameCreate.as_view(), name = 'gameCreate'),
        url(r'^list/$', GameList.as_view(), name = 'gameList'),
        url(r'^(?P<pk>[0-9]+)/$', GameDetail.as_view(), name = 'gameDetail'),
        url(r'^gameplayer/(?P<pk>[0-9]+)/$', GamePlayerUpdate.as_view(), name = 'gamePlayerUpdate'),
        url(r'^player/$', PlayerCreate.as_view(), name = 'playerCreate'),
        url(r'^player/friend$', PlayerFriendCreate.as_view(), name = 'playerFriendCreate'),
        url(r'^player/friend/(?P<pk>[0-9]+)/$', 'player_friend_update', name = 'playerFriendUpdate'),
        url(r'^player/friends$', PlayerFriendsList.as_view(), name = 'playerFriendsList'),
        url(r'^player/(?P<pk>[0-9]+)/$', PlayerUpdate.as_view(), name = 'playerUpdate'),
        url(r'^players/$', PlayerList.as_view(), name = 'playerList'),
        url(r'^players/search/(?P<username>.*)/$', PlayerListSearch.as_view(), name = 'playerListSearch'),
        url(r'^players/(?P<pk>[0-9]+)/$', PlayerDetail.as_view(), name = 'playerDetail'),
        url(r'^sociallogin/(?P<backend>[A-Za-z]+)', 'social_register'),
)


urlpatterns = format_suffix_patterns(urlpatterns)
