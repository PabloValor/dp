from rest_framework import permissions
from .models import GamePlayer

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
          We validate if the game allows to see other predictions
        """
        if not request.method in permissions.SAFE_METHODS:
            return False

        gameplayer_id = view.kwargs['gp']

        try:
          gameplayer = GamePlayer.objects.get(id = gameplayer_id)

          return gameplayer.game.open_predictions

        except (GamePlayer.DoesNotExist) as e:
          return False
