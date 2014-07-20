from rest_framework import generics, permissions, status
from .models import Team, Tournament
from .serializers import TeamSerializer, TournamentSerializer

class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TournamentList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
