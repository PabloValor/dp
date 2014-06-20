from .models import Player

class PlayerAuthenticationBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            player = Player.objects.get(username=username)
            if player.check_password(password):
                return player
        except Player.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return Player.objects.get(pk=user_id)
        except Player.DoesNotExist:
            return None
