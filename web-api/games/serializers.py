from rest_framework import serializers
from .models import Game, Player, GamePlayer, PlayerFriend

class GamePlayerSerializer(serializers.ModelSerializer):
    id = serializers.Field(source = 'player.id')
    username = serializers.Field(source = 'player.username')

    class Meta:
        model = GamePlayer
        fields = ('player', 'username',)

class GameSerializer(serializers.ModelSerializer):
    owner = serializers.Field(source = 'owner.username')
    tournament_name = serializers.Field(source = 'tournament.name')

    gameplayers =  GamePlayerSerializer(source="gameplayer_set", many = True)

    class Meta:
        model = Game
        fields  = ('id', 'owner', 'name', 'tournament', 'tournament_name', 'gameplayers')

class GamePlayerReadOnlySerializer(serializers.ModelSerializer):
    username = serializers.Field(source = 'player.username')

    class Meta:
        model = GamePlayer
        fields = ('player', 'username', 'game', 'player_invitation_status',)

GamePlayerReadOnlySerializer.base_fields['game'] = GameSerializer()

class PlayerSerializer(serializers.ModelSerializer):
#    games = serializers.PrimaryKeyRelatedField(many = True)
#    owner_games = serializers.PrimaryKeyRelatedField(many = True)
#    GamePlayerSerializer.base_fields['player'] = PlayerSerializer()

    class Meta:
        model = Player
        fields = ('id', 'username',)

class IsFriendField(serializers.Field):
    def to_native(self, friends):
        request = self.context['request']
        return request.user in friends

class PlayerSearchSerializer(serializers.ModelSerializer):
    is_friend = IsFriendField(source = 'get_true_friends')
    is_limbo_friend = IsFriendField(source = 'get_limbo_friends')

    class Meta:
        model = Player
        fields = ('id', 'username','is_friend', 'is_limbo_friend')

class PlayerFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerFriend
        fields = ('friend',)

    def validate(self, attrs):
        player = self.context['request'].user
        friend = attrs['friend']

        if player.friends.filter(id = friend.id).exists():
            raise serializers.ValidationError("They are already friends")

        if friend.friends.filter(id = player.id).exists():
            raise serializers.ValidationError("They are already friends")

        return attrs

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
