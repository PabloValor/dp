import json
import redis

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from games.models import GamePlayer, PlayerFriend, Player
from .models import NotificationGame, NotificationFriend
from .serializers import NotificationGameSerializer, NotificationFriendSerializer

from .tasks import send_welcome_email, send_game_notification_email, send_friend_notification_email

def send_notification(token, serializer):
      message =  { 'listener_id': token, 'notification': serializer.data }

      r = redis.StrictRedis(host= settings.REDIS_HOST, port = settings.REDIS_PORT)
      r.publish('notifications', json.dumps(message))

@receiver(post_save, sender=GamePlayer)
def gameplayer_creation_notification(sender, instance=None, created=False, **kwargs):
    if instance.player == instance.game.owner:
        return

    notification_type = ''
    send_mail = False
    if (created or instance.is_invited()):
        # A player is being invitaded to play
        notification_type = '1'
        player = instance.player
        sender = instance.game.owner

        send_mail = True

        # If the owner of the game is inviting again a player who rejected to play
        # We desactivate the first notification where the owner invited him
        if not created and instance.is_invited():
          try:
            old_notification = NotificationGame.objects.filter(notification_type = '1', player = player, sender = sender, active = True).latest('pk')
            old_notification.active = False
            old_notification.save()
          except NotificationGame.DoesNotExist as e:
            # Could be that the user already desactivated all the notifications
            pass

    elif instance.is_answered_request():
        # A player answered the request to play
        # If he accepts '2' if he rejects '3'
        notification_type = '2' if instance.status else '3'
        player = instance.game.owner
        sender = instance.player

    elif instance.is_another_chance():
        # A player asks for antother invitation
        notification_type = '4'
        player = instance.game.owner
        sender = instance.player

    if notification_type:
        notification = NotificationGame(player = player, 
                                        sender = sender,
                                        notification_type = notification_type,
                                        game_id = instance.game.id)

        notification.save()

        serializer = NotificationGameSerializer(notification)
        send_notification(player.auth_token.key, serializer)


        # We only send a mail if a player is being invited
        if send_mail:
            send_game_notification_email.delay(player.email, sender.username, instance.game.name)


@receiver(post_save, sender=PlayerFriend)
def playerfriend_creation_notification(sender, instance=None, created=False, **kwargs):
    notification_type = ''
    send_mail = False

    if created:
        # A player is being being request to be a Friend
        notification_type = '1'
        player = instance.friend
        sender = instance.player

        send_mail = True

    elif instance.status:
        # A player accepts to be a friend, so we notify the requested
        notification_type = '2'
        player = instance.player
        sender = instance.friend

    if notification_type:
        notification = NotificationFriend(player = player, 
                                          sender = sender,
                                          notification_type = notification_type)

        notification.save()

        serializer = NotificationFriendSerializer(notification)
        send_notification(player.auth_token.key, serializer)

        # We only send a mail if a player is sending a friend request
        if send_mail:
            send_friend_notification_email.delay(player.email, sender.username)

@receiver(post_save, sender=Player)
def player_creation_welcome_email(sender, instance=None, created=False, **kwargs):
    send_welcome_email.delay({'username': instance.username, 'email': instance.email })

