from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GameList, GameDetail

urlpatterns = patterns('games.views',
        url(r'^$', GameList.as_view()),
        url(r'^(?P<pk>[0-9]+)/$', GameDetail.as_view())
)


urlpatterns = format_suffix_patterns(urlpatterns)
