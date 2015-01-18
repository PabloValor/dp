from rest_framework import serializers
from .models import Team, Tournament, Fixture, Match

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'crest')

class MatchSerializer(serializers.ModelSerializer):
    visitor_team = TeamSerializer()
    local_team = TeamSerializer()
    winner = serializers.BooleanField(source = 'get_winner')

    class Meta:
        model = Match
        #date, local_team, local_team_goals, visitor_team, visitor_team_goals fixture, suspended, is_classic,

class FixtureSerializer(serializers.ModelSerializer):
    matches = MatchSerializer(many = True)
    is_closed = serializers.BooleanField()

    class Meta:
        model = Fixture
        fields = ('number', 'is_finished', 'matches', 'is_closed')

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('id', 'name', )

class TournamentTeamsSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many = True)

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'teams',)        

class TournamentFixtureSerializer(serializers.ModelSerializer):
    fixtures = FixtureSerializer(many = True)
    current_fixture = FixtureSerializer(source = "get_current_fixture")
    is_finished = serializers.BooleanField()

    class Meta:
        model = Tournament
        fields = ('id', 'fixtures', 'current_fixture', 'is_finished')

class TournamentNextFixtureSerializer(serializers.ModelSerializer):
    fixture = FixtureSerializer(source = "get_next_fixture")
    tournament_name = serializers.CharField(source = 'name')

    class Meta:
        model = Tournament
        fields = ('fixture', 'tournament_name')

class TournamentCurrentOrLastFixtureSerializer(serializers.ModelSerializer):
    fixture = FixtureSerializer(source = "get_current_or_last_fixture")
    tournament_name = serializers.CharField(source = 'name')

    class Meta:
        model = Tournament
        fields = ('fixture', 'tournament_name')

class TeamStatsField(serializers.Field):
    def to_representation(self, team):
        tournament =  self.root.instance
        return team.get_tournament_stats(tournament)
    
class TeamStatsSerializer(serializers.ModelSerializer):
    stats = TeamStatsField(source = '*')
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'crest', 'stats')        

class TournamentStatsSerializer(serializers.ModelSerializer):
    teams = TeamStatsSerializer(many = True)

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'teams',)
