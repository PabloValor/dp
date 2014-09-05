from rest_framework import serializers
from games.serializers import PlayerSerializer, GamePlayerSerializer, PlayerFriendSerializer
from .models import NotificationFriend, NotificationGame

class NotificationGameSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(source="player", read_only = True)
    sender = PlayerSerializer(source="sender", read_only = True)
    game_id = serializers.Field(source="game.id")

    class Meta:
        model = NotificationGame
        fields = ('notification_type', 'player', 'game_id', 'sender')
        read_only_fields = ('notification_type', )

class NotificationFriendSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(source="player", read_only = True)
    sender = PlayerSerializer(source="sender", read_only = True)

    class Meta:
        model = NotificationFriend
        fields = ('notification_type', 'player', 'sender')
        read_only_fields = ('notification_type',)
