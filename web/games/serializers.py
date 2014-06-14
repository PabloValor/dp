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
        fields = ('username', 'games', 'owner_games')

class PlayerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('username', 'email', 'password')

    def restore_object(self, attrs, instance = None):
        # Retrieves
        if instance:
            instance.username = attrs.get('username', instance.username)
            instance.email = attrs.get('email', instance.email)
        # Creates
        else:
            request = self.context['request']
            if request.user.is_anonymous:
                instance = Player(email=attrs['email'], username=attrs['username'])
                instance.set_password(attrs['password'])

        return instance

class PlayerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('games',)
