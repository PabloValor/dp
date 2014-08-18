from rest_framework import generics, permissions, status
from .models import Team, Tournament, Fixture
from .serializers import TeamSerializer, TournamentSerializer, TournamentFixtureSerializer

class TournamentList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class TournamentFixtureList(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TournamentFixtureSerializer
    queryset = Tournament.objects.all()
