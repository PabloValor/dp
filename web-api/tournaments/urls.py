from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TeamList, TeamDetail

urlpatterns = patterns('tournaments.views',
        url(r'^teams/$', TeamList.as_view()),
        url(r'^teams/(?P<pk>[0-9]+)/$', TeamDetail.as_view())
)


urlpatterns = format_suffix_patterns(urlpatterns)
