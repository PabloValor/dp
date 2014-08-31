from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from games.models import GamePlayer, PlayerFriend
from .models import NotificationGame, NotificationFriend

@receiver(post_save, sender=GamePlayer)
def gameplayer_creation_notification(sender, instance=None, created=False, **kwargs):
    notification_type = ''
    if created and not instance.player == instance.game.owner:
        # A player is being invitaded to play
        notification_type = '1'
        player = instance.player

    elif not instance.status == None and instance.another_chance == None:
        # A player answered the request to play
        # If he accepts '2' if he rejects '3'
        notification_type = '2' if instance.status else '3'
        player = instance.game.owner

    elif instance.another_chance and instance.status == False:
        # A player asks for antother invitation
        notification_type = '4'
        player = instance.game.owner

    if notification_type:
        notification = NotificationGame(player = player, 
                                        notification_type = notification_type,
                                        gameplayer = instance)

        notification.save()


@receiver(post_save, sender=PlayerFriend)
def playerfriend_creation_notification(sender, instance=None, created=False, **kwargs):
    notification_type = ''

    if created:
        # A player is being being request to be a Friend
        notification_type = '1'
        player = instance.friend

    elif instance.status:
        # A player accepts to be a friend, so we notify the requested
        notification_type = '2'
        player = instance.player

    if notification_type:
        notification = NotificationFriend(player = player, 
                                          notification_type = notification_type,
                                          playerfriend = instance)

        notification.save()
