from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = patterns('notifications.views',
        url(r'^(?P<pk>[0-9]+)/(?P<notification_type>[a-z]+)$', 'notification_update', name = 'notificationUpdate'),
        url(r'^email$', 'email'),
)


urlpatterns = format_suffix_patterns(urlpatterns)
