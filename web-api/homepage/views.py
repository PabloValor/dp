from django.shortcuts import render
from rest_framework import generics, permissions, status
from tournaments.serializers import TournamentSerializer
from .models import TournamentHomepage, News
from .serializers import NewsSerializer

class TournamentHomepageList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TournamentSerializer
    
    def get_queryset(self):
        tournamentHomepageList = TournamentHomepage.objects.all()        
        return [x.tournament for x in tournamentHomepageList]

class NewsList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NewsSerializer
    queryset = News.objects.filter(active = True)
