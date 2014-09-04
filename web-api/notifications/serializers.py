from rest_framework import serializers
from .models import NotificationFriend, NotificationGame
from games.serializers import PlayerSerializer, GamePlayerSerializer, PlayerFriendSerializer

class NotificationGameSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(source="player")
    sender = PlayerSerializer(source="sender")

    class Meta:
        model = NotificationGame
        fields = ('notification_type', 'player', 'game_id', 'sender')

class NotificationFriendSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(source="player")
    sender = PlayerSerializer(source="sender")

    class Meta:
        model = NotificationFriend
        fields = ('notification_type', 'player', 'sender',)
