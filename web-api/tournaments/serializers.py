from rest_framework import serializers
from .models import Team, Tournament, Fixture, Match

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'crest')

class MatchSerializer(serializers.ModelSerializer):
    visitor_team = TeamSerializer(source = 'visitor_team')
    local_team = TeamSerializer(source = 'local_team')
    winner = serializers.Field(source = 'get_winner')

    class Meta:
        model = Match
        #date, local_team, local_team_goals, visitor_team, visitor_team_goals fixture, suspended, is_classic,

class FixtureSerializer(serializers.ModelSerializer):
    matches = MatchSerializer(source = 'matches', many = True)
    is_closed = serializers.Field(source = 'is_closed')

    class Meta:
        model = Fixture
        fields = ('number', 'is_finished', 'matches', 'is_closed')

class TournamentSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(source = 'get_teams', many = True)

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'teams',)

class TournamentFixtureSerializer(serializers.ModelSerializer):
    fixtures = FixtureSerializer(source="fixtures", many = True)
    current_fixture = FixtureSerializer(source = "get_current_fixture")
    is_finished = serializers.Field(source = 'is_finished')

    class Meta:
        model = Tournament
        fields = ('id', 'fixtures', 'current_fixture', 'is_finished')

class TournamentNextFixtureSerializer(serializers.ModelSerializer):
    fixture = FixtureSerializer(source = "get_next_fixture")
    tournament_name = serializers.Field(source = 'name')

    class Meta:
        model = Tournament
        fields = ('fixture', 'tournament_name')

class TournamentCurrentOrLastFixtureSerializer(serializers.ModelSerializer):
    fixture = FixtureSerializer(source = "get_current_or_last_fixture")
    tournament_name = serializers.Field(source = 'name')

    class Meta:
        model = Tournament
        fields = ('fixture', 'tournament_name')

class TeamStatsField(serializers.Field):
    def to_native(self, team):
        tournament =  self.root.object
        return team.get_tournament_stats(tournament)
    
class TeamStatsSerializer(serializers.ModelSerializer):
    stats = TeamStatsField(source = '*')
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'crest', 'stats')        

class TournamentStatsSerializer(serializers.ModelSerializer):
    teams = TeamStatsSerializer(source = 'get_teams', many = True)

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'teams',)
