from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .models import GamePlayer
from tournaments.models import Match

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user

class IsSameUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == 'PUT' and  obj == request.user

class IsFriend(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == 'PUT' and  obj.friend == request.user

class SameGamePlaying(permissions.BasePermission):
    def has_permission(self, request, view):
        """
          We validate if the user is playing the game of the predictions he is asking
        """
        if not request.method in permissions.SAFE_METHODS:
            return False

        gameplayer_id = view.kwargs['gp']

        try:
          gameplayer = GamePlayer.objects.get(id = gameplayer_id)
          player = request.user
          player_gameplayer = player.gameplayer_set.get(game = gameplayer.game)

          return player_gameplayer.status

        except (GamePlayer.DoesNotExist) as e:
          return False

class OpenGame(permissions.BasePermission):
    def has_permission(self, request, view):
        """
          We validate if the game allows the gameplayer's prediction
        """
        if not request.method in permissions.SAFE_METHODS:
            return False

        gameplayer_id = view.kwargs['gp']

        try:
          gameplayer = GamePlayer.objects.get(id = gameplayer_id)
          # If the user is asking for his predictions
          if gameplayer.player == request.user:
            return True

          # If not we check if the game allows to see other players predictions
          return gameplayer.game.open_predictions

        except (GamePlayer.DoesNotExist) as e:
          return False

class PlayerMatchPredictionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        """
          We validate if the player can create new match predictions
        """
        player = request.user
        gameplayer_id = request.DATA['gameplayer']
        gameplayer = get_object_or_404(GamePlayer, pk = gameplayer_id)

        # If the user is trying to update another's prediction
        if player != gameplayer.player:
          return False

        # If the user is not playing this game
        if not gameplayer.status:
          return False

        match_id = request.DATA['match']
        match = get_object_or_404(Match, pk = match_id)

        # If the match has already finished.
        if match.is_finished:
          return False

        # If the fixture has already finished.
        if match.fixture.is_finished:
          return False

        # If the fixture is close for new predictions
        if match.fixture.is_closed():
          return False

        return True


