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
        write_only_fields = ('password',) 
        fields = ('username', 'email', 'password')

    def validate_email(self, attrs, source):
        if not attrs['email']:
            raise serializers.ValidationError('The email field is required.')
        else:
            if Player.objects.filter(email = attrs[source]).exists():
                raise serializers.ValidationError('There is a user with the same email.')

        return attrs

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
