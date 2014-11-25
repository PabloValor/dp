from rest_framework import generics, permissions, status
from .models import Team, Tournament, Fixture
from .serializers import (TeamSerializer, TournamentSerializer, TournamentFixtureSerializer,
                          TournamentNextFixtureSerializer, TournamentCurrentOrLastFixtureSerializer)

class TournamentList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()

class TournamentFixtureList(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TournamentFixtureSerializer
    queryset = Tournament.objects.all()

class AllTournamentNextFixtureList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TournamentNextFixtureSerializer
    queryset = Tournament.objects.filter(is_finished = False)

class AllTournamentCurrentOrLastFixtureList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TournamentCurrentOrLastFixtureSerializer
    queryset = Tournament.objects.filter(is_finished = False)        
