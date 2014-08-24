from rest_framework import serializers
from django.db.models import Q
from .models import Game, Player, GamePlayer, PlayerFriend, PlayerMatchPrediction
from tournaments.models import Match
from tournaments.serializers import MatchSerializer


class GamePlayerSerializer(serializers.ModelSerializer):
    player_id = serializers.Field(source = 'player.id')
    username = serializers.Field(source = 'player.username')

    class Meta:
        model = GamePlayer
        fields = ('player', 'username', 'status', 'another_chance', 'id', 'initial_points', )

class GamePlayerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePlayer
        fields = ('status',)

class GamePlayerUpdateAnotherChanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePlayer
        fields = ('another_chance',)

class GamePlayerUpdateInvitesAgainSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePlayer
        fields = ('another_chance', 'status')

    def validate(self, attrs):
        view =  self.context['view']
        if view.object == None:
          raise serializers.ValidationError("Empty list")

        return attrs

class GamePlayerCreateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs.pop('many', True)
        super(GamePlayerCreateSerializer, self).__init__(many=True, *args, **kwargs)

    class Meta:
        model = GamePlayer
        fields = ('player','game', 'initial_points', )

    def validate(self, attrs):
        # Because of the Many = True this break up the validations and attrs only matches the first user
        game_owner = self.context['request'].user
        game = attrs['game']
        player = attrs['player']
        
        if player == game_owner:
          raise serializers.ValidationError("It's the same user")
        elif game_owner != game.owner:
          raise serializers.ValidationError("It's the game owner")
        elif player.games.filter(id = game.id).exists():
          raise serializers.ValidationError("It's already playing")
        elif not game_owner.is_friend(player):
          raise serializers.ValidationError("They are not friends")

        return attrs

class UserGamePlayerField(serializers.Field):
    def to_native(self, gameplayers):
        if self.context:
          user = self.context['request'].user
          gameplayer = gameplayers.filter(player = user)
          return gameplayer.values('id', 'player__username', 'status', 'another_chance', 'initial_points', )

class GameSerializer(serializers.ModelSerializer):
    owner = serializers.Field(source = 'owner.username')
    tournament_name = serializers.Field(source = 'tournament.name')
    gameplayers = GamePlayerSerializer(source="gameplayer_set", many = True)
    you = UserGamePlayerField(source = 'gameplayer_set')

    def validate(self, attrs):
        game_owner = self.context['request'].user
        gameplayers = attrs['gameplayer_set']

        if gameplayers:
          players_ids = [gp.player.id for gp in gameplayers]

          for gp in gameplayers:
            if gp.player == game_owner:
              continue

            if players_ids.count(gp.player.id) > 1:
              raise serializers.ValidationError("Duplicate users")

            if not game_owner.is_friend(gp.player):
              raise serializers.ValidationError("There is someone that is not a friend")

        return attrs


    class Meta:
        model = Game
        fields  = ('id', 'owner', 'name', 'tournament', 'tournament_name', 
                    'gameplayers', 'you', 'classic', 'points_exact', 
                    'points_general',  'points_classic',  'points_double', )

class PlayerMatchPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerMatchPrediction

    def validate(self, attrs):
        player = self.context['request'].user
        gameplayer = attrs['gameplayer']
        if player != gameplayer.player:
          raise serializers.ValidationError("You are trying to update another's prediction")

        if not gameplayer.status:
          raise serializers.ValidationError("You are not playing this game")

        match = attrs['match']
        if match.is_finished:
          raise serializers.ValidationError('Match has already finished.')

        if match.fixture.is_finished:
          raise serializers.ValidationError('Fixture has already finished.')

        if match.fixture.is_playing():
          raise serializers.ValidationError('Fixture is already being played')

        return attrs

class PlayerMatchPredictionListSerializer(serializers.ModelSerializer):
    match = MatchSerializer(source="match")
    points = serializers.Field(source = "get_points")

    class Meta:
        model = PlayerMatchPrediction

class PlayerSerializer(serializers.ModelSerializer):
#    games = serializers.PrimaryKeyRelatedField(many = True)
#    owner_games = serializers.PrimaryKeyRelatedField(many = True)

    class Meta:
        model = Player
        fields = ('id', 'username',)

class IsFriendField(serializers.Field):
    def to_native(self, friends):
        request = self.context['request']
        return request.user in friends

class PlayerSearchSerializer(serializers.ModelSerializer):
    is_friend = IsFriendField(source = 'get_true_friends')
    is_limbo_friend = IsFriendField(source = 'get_ignored_friends')
    is_waiting_for_you = IsFriendField(source = 'get_friends_that_ignored_us')
    is_bad_friend = IsFriendField(source = 'get_friends_we_rejected')
    you_are_bad_friend = IsFriendField(source = 'get_bad_friends')

    class Meta:
        model = Player
        fields = ('id', 'username','is_friend', 'is_limbo_friend', 'is_waiting_for_you','is_bad_friend', 'you_are_bad_friend')

class PlayerFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerFriend
        fields = ('friend',)

    def validate(self, attrs):
        friend_asking = self.context['request'].user
        friend = attrs['friend']

        # If he had already asks we raise an error. It doesn't matter if they are friends or not. 
        if friend_asking.friend_player.filter(friend__id = friend.id).exists():
            raise serializers.ValidationError("They are already friends")

        # If he is already a friend or if he hasn't answer the request of his friend and wants to 
        # create a new request we raise an error.
        # If he has rejected his friend and wants to create a new request is OK.
        if friend.friend_player.filter(Q(status = None) | Q(status = True), friend__id = friend_asking.id).exists():
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
