from rest_framework import serializers
from .models import NotificationFriend, NotificationGame
from games.serializers import PlayerSerializer, GamePlayerSerializer, PlayerFriendSerializer

class NotificationGameSerializer(serializers.ModelSerializer):
    gameplayer = GamePlayerSerializer(source="gameplayer")
    player = PlayerSerializer(source="player")

    class Meta:
        model = NotificationGame
        fields = ('notification_type', 'player', 'game_id', 'sender')

class NotificationFriendSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(source="player")
    playerfriend = PlayerFriendSerializer(source="player")

    class Meta:
        model = NotificationFriend
        fields = ('notification_type', 'player', 'sender',)
