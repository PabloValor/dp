from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GameList, GameDetail, PlayerList, PlayerDetail

urlpatterns = patterns('games.views',
        url(r'^$', GameList.as_view()),
        url(r'^(?P<pk>[0-9]+)/$', GameDetail.as_view()),
        url(r'^players/$', PlayerList.as_view()),
        url(r'^players/(?P<pk>[0-9]+)/$', PlayerDetail.as_view()),
)


urlpatterns = format_suffix_patterns(urlpatterns)
