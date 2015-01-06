from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = patterns('homepage.views',
        url(r'^tournaments$', TournamentHomepageList.as_view(), name = 'tournamentHomepageList'),
        url(r'^news$', NewsList.as_view(), name = 'newsList'),                       
)

urlpatterns = format_suffix_patterns(urlpatterns)
