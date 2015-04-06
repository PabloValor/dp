from rest_framework import serializers
from django.db.models import Q
from .models import Game, Player, GamePlayer, PlayerFriend, PlayerMatchPrediction, FixturePlayerPoints
from tournaments.models import Match
from tournaments.serializers import MatchSerializer, FixtureMinimalSerializer


class FixturePlayerPointsSerializer(serializers.ModelSerializer):
    fixture_number = serializers.IntegerField(source = 'fixture.number')

    class Meta:
        model = FixturePlayerPoints
        fields = ('fixture_number', 'points', 'classic_prediction')

class GamePlayerSerializer(serializers.ModelSerializer):
    player_id = serializers.IntegerField(source = 'player.id', read_only = True)
    username = serializers.CharField(source = 'player.username', read_only = True)
    fixture_points = FixturePlayerPointsSerializer(source="fixtureplayerpoints_set", many = True, read_only = True)

    class Meta:
        model = GamePlayer
        fields = ('player', 'username', 'status', 'another_chance', 'id', 'initial_points', 'fixture_points', 'player_id')

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
        if self.instance == None:
          raise serializers.ValidationError("Empty list")

        return attrs

class GamePlayerCreateSerializer(serializers.ModelSerializer):
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
    def to_representation(self, gameplayers):
        if self.context:
          user = self.context['request'].user
          gameplayer = gameplayers.filter(player = user)
          return gameplayer.values('id', 'player__username', 'status', 'another_chance', 'initial_points', )

class GameSerializer(serializers.ModelSerializer):
    gameplayers = GamePlayerSerializer(source="gameplayer_set", many = True)
    you = UserGamePlayerField(source = 'gameplayer_set', read_only = True)
    
    owner = serializers.CharField(source = 'owner.username', read_only = True)
    tournament_name = serializers.CharField(source = 'tournament.name', read_only = True)
    tournament_id = serializers.CharField(source = 'tournament.id', read_only = True)
    current_fixture = FixtureMinimalSerializer(source = 'tournament.get_current_fixture', read_only = True)
    last_fixture_number = serializers.IntegerField(source = 'tournament.get_last_fixture_number', read_only = True)

    def validate(self, attrs):
        game_owner = self.context['request'].user
        gameplayers = attrs['gameplayer_set']

        if gameplayers:
          players_ids = [gp['player'].id for gp in gameplayers]

          for gp in gameplayers:
            player = gp['player']
            if player == game_owner:
              continue

            if players_ids.count(player.id) > 1:
              raise serializers.ValidationError("Duplicate users")

            if not game_owner.is_friend(player):
              raise serializers.ValidationError("There is someone that is not a friend")

        return attrs


    def create(self, validated_data):
        request = self.context['request']
        gameplayerList = validated_data.pop('gameplayer_set')

        game = Game(**validated_data)
        game.owner = request.user
        game.save()

        for gameplayer in gameplayerList:
            player = gameplayer['player']
            # The status needs to be None and not False
            status = None
            
            if player == game.owner:
                status = True
                
            game_player = GamePlayer.objects.create(player = player,
                                                    game = game,
                                                    status = status,
                                                    initial_points = gameplayer.get('initial_points', 0))
        
        return game


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance
        
    class Meta:
        model = Game
        fields  = ('id', 'owner', 'name', 'tournament', 'tournament_name', 'tournament_id',
                    'gameplayers', 'you', 'classic', 'points_exact', 'open_predictions',
                    'points_general',  'points_classic',  'points_double', 'last_fixture_number',
                    'current_fixture')

class PlayerMatchPredictionSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
      PlayerMatchPrediction.objects.filter(match = validated_data['match'],
                                           gameplayer = validated_data['gameplayer']).delete()

      player_match_prediction = PlayerMatchPrediction.objects.create(**validated_data)

      return player_match_prediction
    
    class Meta:
        model = PlayerMatchPrediction

class PlayerMatchPredictionListSerializer(serializers.ModelSerializer):
    match = MatchSerializer()
    points = serializers.IntegerField(source = "get_points")

    class Meta:
        model = PlayerMatchPrediction
        fields = ('local_team_goals', 'visitor_team_goals', 'points', 'id', 'match')

class PlayerSerializer(serializers.ModelSerializer):
#    games = serializers.PrimaryKeyRelatedField(many = True)
#    owner_games = serializers.PrimaryKeyRelatedField(many = True)

    class Meta:
        model = Player
        fields = ('id', 'username',)

class IsFriendField(serializers.Field):
    def to_representation(self, friends):
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

    def create(self, validated_data):
        player = self.context['request'].user
        friend = validated_data['friend']        

        instance = PlayerFriend.objects.create(player = player, friend = friend)

        # If the player who rejected the last invitation creates a new one
        # we delete the old one (maybe in the future we will like to save this info)
        PlayerFriend.objects.filter(friend =  player, player = friend, status = False).delete()

        return instance

class PlayerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        write_only_fields = ('password',) 
        fields = ('username', 'email', 'password')

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('The email field is required.')
        elif Player.objects.filter(email = value).exists():
                raise serializers.ValidationError('There is a user with the same email.')

        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError('The password field is required.')
        elif len(value) < 8:
            raise serializers.ValidationError('The password has to have 8 characters.')
        return value

    def create(self, validated_data):
        request = self.context['request']
        if request.user.is_anonymous:
            instance = Player(email=validated_data['email'], username=validated_data['username'])
            instance.set_password(validated_data['password'])
            instance.save()

        return instance

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance    

class PlayerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('games',)
