from django.test import TestCase
from .models import NotificationGame, NotificationFriend
from games.factories import GamePlayerFactory, GameFactory, PlayerFriendFactory

class GameNotificationTest(TestCase):
    def test_gameplayer_creation_notification(self):
        """ 
          When a Gameplayer is created we create a Notification
        """
        gp = GamePlayerFactory()
        self.assertEqual(NotificationGame.objects.count(), 1)
        self.assertEqual(NotificationGame.objects.first().player, gp.player)
        self.assertEqual(NotificationGame.objects.first().notification_type, '1')

    def test_gameplayer_creation_notification_B(self):
        """ 
          When a Gameplayer is created but the player is the owner
          we don't create a notification for the player

        """
        game = GameFactory()
        gp = GamePlayerFactory(game = game, player = game.owner)
        self.assertEqual(NotificationGame.objects.count(), 0)

    def test_gameplayer_update_notification_A(self):
        """ 
          When a Gameplayer status is updated we create a Notification

          Gameplayer accepts to play
        """
        gp = GamePlayerFactory()
        gp.status = True
        gp.save()

        self.assertEqual(NotificationGame.objects.count(), 2)
        self.assertEqual(NotificationGame.objects.all()[1].notification_type, '2')
        self.assertEqual(NotificationGame.objects.all()[1].player, gp.game.owner)

    def test_gameplayer_update_notification_B(self):
        """ 
          When a Gameplayer status is updated we create a Notification

          Gameplayer rejects to play
        """
        gp = GamePlayerFactory()
        gp.status = False
        gp.save()

        self.assertEqual(NotificationGame.objects.count(), 2)
        self.assertEqual(NotificationGame.objects.all()[1].notification_type, '3')
        self.assertEqual(NotificationGame.objects.all()[1].player, gp.game.owner)

    def test_gameplayer_update_notification_C(self):
        """ 
          When a Gameplayer another_chance is updated we create a Notification

          Gameplayer asks for another chance to play
        """
        gp = GamePlayerFactory(status = False)
        gp.another_chance = True
        gp.save()

        self.assertEqual(NotificationGame.objects.count(), 2)
        self.assertEqual(NotificationGame.objects.all()[1].notification_type, '4')
        self.assertEqual(NotificationGame.objects.all()[1].player, gp.game.owner)

    def test_gameplayer_update_notification_D(self):
        """ 
          When a Gameplayer another_chance is updated with False we
          do not create a new notification

          Because he alread has rejected to play, now he don't wants to see
          the game in his list
        """
        gp = GamePlayerFactory(status = False)
        gp.another_chance = False
        gp.save()

        self.assertEqual(NotificationGame.objects.count(), 1)

    def test_gameplayer_update_notification_E(self):
        """ 
          When a Gameplayer another_chance is updated but he hasn't answer if he
          plays or not we dont create a Notification
        """
        gp = GamePlayerFactory(status = None)
        gp.another_chance = True
        gp.save()

        self.assertEqual(NotificationGame.objects.count(), 1)

class FriendNotificationTest(TestCase):
    def test_playerfriend_creation_notification(self):
        """ 
          When a Friend request is created we create a Notification
        """
        pf = PlayerFriendFactory()

        self.assertEqual(NotificationFriend.objects.count(), 1)
        self.assertEqual(NotificationFriend.objects.first().player, pf.friend)
        self.assertEqual(NotificationFriend.objects.first().notification_type, '1')

    def test_playerfriend_update_notification(self):
        """ 
          A friend accepts to be a friend
        """
        pf = PlayerFriendFactory()
        pf.status = True
        pf.save()

        self.assertEqual(NotificationFriend.objects.count(), 2)
        self.assertEqual(NotificationFriend.objects.all()[1].player, pf.player)
