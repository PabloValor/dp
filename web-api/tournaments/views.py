from rest_framework import generics, permissions, status
from .models import Team, Tournament, Fixture
from .serializers import (TeamSerializer, TournamentSerializer, TournamentFixtureSerializer,
                          TournamentNextFixtureSerializer, TournamentCurrentOrLastFixtureSerializer,
                          TournamentStatsSerializer, TournamentTeamsSerializer, FixtureSerializer)

class TournamentList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()

class TournamentTeamsList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TournamentTeamsSerializer
    queryset = Tournament.objects.all()    

class TournamentAllFixtures(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TournamentFixtureSerializer
    queryset = Tournament.objects.all()

class TournamentFixture(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FixtureSerializer
    queryset = Fixture.objects.all()

class TournamentFixtureByNumber(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FixtureSerializer

    def get_object(self):
        user = self.request.user
        tournament_id = self.kwargs['pk']
        fixture_number = self.kwargs['number']

        try:
            fixture = Fixture.objects.get(tournament__id = tournament_id, number = fixture_number)
            return fixture
        except Fixture.DoesNotExist as e:
            raise Http404

class AllTournamentNextFixtureList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TournamentNextFixtureSerializer
    queryset = Tournament.objects.filter(is_finished = False)

class AllTournamentCurrentOrLastFixtureList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TournamentCurrentOrLastFixtureSerializer
    queryset = Tournament.objects.filter(is_finished = False)

class TournamentStats(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TournamentStatsSerializer
    queryset = Tournament.objects.all()    
