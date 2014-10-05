from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = patterns('contact.views',
        url(r'^$', ContactCreate.as_view(), name = 'contactCreate'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
