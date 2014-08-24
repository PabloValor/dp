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
    matches = MatchSerializer(source = 'matches', many=True)
    is_playing = serializers.Field(source = 'is_playing')

    class Meta:
        model = Fixture
        fields = ('number', 'is_finished', 'matches', 'is_playing')

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

