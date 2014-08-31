from django.db import models
from games.models import Player, GamePlayer, PlayerFriend

class NotificationModel(models.Model):
    TYPES = ()

    sender = models.ForeignKey(Player)
    notification_type = models.CharField(max_length=1, choices=TYPES, default='1')
    active = models.BooleanField(default = True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

class NotificationGame(NotificationModel):
    player = models.ForeignKey(Player, related_name = 'game_notifications')
    TYPES = (
        ('1', 'Game Invitation'),
        ('2', 'Game Invitation Accepted'),
        ('3', 'Game Invitation Rejected'),
        ('4', 'Game Another Chance'),
    )
    game_id = models.PositiveIntegerField(blank=True, null=True)

class NotificationFriend(NotificationModel):
    player = models.ForeignKey(Player, related_name = 'friend_notifications')
    TYPES = (
        ('1', 'Friend Invitation'),
        ('2', 'Friend Invitation Accepted'),
    )
