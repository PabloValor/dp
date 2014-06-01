from rest_framework import serializers
from .models import Game, Player

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields  = ('id', 'name', 'tournament')

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'username')
