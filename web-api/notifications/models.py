from django.db import models
from games.models import Player, GamePlayer, PlayerFriend

class NotificationModel(models.Model):
    TYPES = ()

    notification_type = models.CharField(max_length=1, choices=TYPES, default='1')
    player = models.ForeignKey(Player)
    active = models.BooleanField(default = False)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

class NotificationGame(NotificationModel):
    TYPES = (
        ('1', 'Game Invitation'),
        ('2', 'Game Invitation Accepted'),
        ('3', 'Game Invitation Rejected'),
        ('4', 'Game Another Chance'),
    )
    gameplayer = models.ForeignKey(GamePlayer, blank=True, null=True)

class NotificationFriend(NotificationModel):
    TYPES = (
        ('1', 'Friend Invitation'),
        ('2', 'Friend Invitation Accepted'),
    )

    playerfriend = models.ForeignKey(PlayerFriend, blank=True, null=True) 
