from rest_framework import serializers
from .models import Game, Player

class GameSerializer(serializers.ModelSerializer):
    owner = serializers.Field(source = 'owner.username')

    class Meta:
        model = Game
        fields  = ('id', 'owner', 'name', 'tournament', 'players')

class PlayerSerializer(serializers.ModelSerializer):
#    games = serializers.PrimaryKeyRelatedField(many = True)
#    owner_games = serializers.PrimaryKeyRelatedField(many = True)

    class Meta:
        model = Player
        fields = ('id', 'username', 'games', 'owner_games')
