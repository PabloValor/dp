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

    def test_gameplayer_creation_notification_C(self):
        """ 
          When a Gameplayer is created but the player is the owner
          we don't create a notification for the player

        """
        game = GameFactory()
        gp = GamePlayerFactory(game = game, player = game.owner, status = True)
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
          
          There is one notification because of the creation of the game
        """
        gp = GamePlayerFactory(status = False)
        gp.another_chance = False
        gp.save()

        self.assertEqual(NotificationGame.objects.count(), 1)

    def test_gameplayer_update_notification_E(self):
        """ 
          When a Gameplayer another_chance is updated we create a Notification

          Owner invites Gameplayer again after he had asked for another chance to play
        """

        # Player invited
        gp = GamePlayerFactory()
        self.assertEqual(NotificationGame.objects.count(), 1)
        self.assertEqual(NotificationGame.objects.filter(player = gp.player).count(), 1)

        # Player rejects 
        gp.status = False
        gp.save()
        self.assertEqual(NotificationGame.objects.filter(player = gp.player).count(), 1)
        self.assertEqual(NotificationGame.objects.count(), 2)

        # Player asks for another chance
        gp.another_chance = True
        gp.save()
        self.assertEqual(NotificationGame.objects.filter(player = gp.player).count(), 1)
        self.assertEqual(NotificationGame.objects.count(), 3)

        # Player invites again the user
        gp.reset()
        gp.save()
        self.assertEqual(NotificationGame.objects.filter(player = gp.player).count(), 2)
        self.assertEqual(NotificationGame.objects.filter(player = gp.player, active = True).count(), 1)
        self.assertEqual(NotificationGame.objects.count(), 4)

    def test_gameplayer_update_notification_F(self):
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

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from games.factories import PlayerFactory
from .factories import NotificationGameFactory, NotificationFriendFactory

class NotificationAPITest(APITestCase):
    def test_update_notification_202_ACCEPTED_A(self):
        """ 
          Nico updates Game Notification 
        """
        nico = PlayerFactory()
        notification = NotificationGameFactory(player = nico)
        self.assertTrue(NotificationGame.objects.get(pk = notification.pk).active)

        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('notificationUpdate', kwargs = {'pk': notification.pk, 'notification_type': 'game' })
        response = self.client.put(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertFalse(NotificationGame.objects.get(pk = notification.pk).active)
        self.assertEqual(NotificationGame.objects.all().count(), 1)

    def test_update_notification_202_ACCEPTED_B(self):
        """ 
          Nico updates Friend Notification 
        """
        nico = PlayerFactory()
        notification = NotificationFriendFactory(player = nico)
        self.assertTrue(NotificationFriend.objects.get(pk = notification.pk).active)

        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('notificationUpdate', kwargs = {'pk': notification.pk, 'notification_type': 'friend' })
        response = self.client.put(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertFalse(NotificationFriend.objects.get(pk = notification.pk).active)
        self.assertEqual(NotificationFriend.objects.all().count(), 1)

    def test_update_notification_404_NOT_FOUND_A(self):
        """ 
            Nico tries to update a Friend Notification but it is a Game Notification
        """ 
        nico = PlayerFactory()
        notification = NotificationGameFactory(player = nico)
        self.assertTrue(NotificationGame.objects.get(pk = notification.pk).active)

        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('notificationUpdate', kwargs = {'pk': notification.pk, 'notification_type': 'friend' })
        response = self.client.put(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(NotificationGame.objects.get(pk = notification.pk).active)
        self.assertEqual(NotificationGame.objects.all().count(), 1)

    def test_update_notification_404_NOT_FOUND_B(self):
        """ 
            Nico tries to update a Game Notification but it is a Friend Notification
        """
        nico = PlayerFactory()
        notification = NotificationFriendFactory(player = nico)
        self.assertTrue(NotificationFriend.objects.get(pk = notification.pk).active)

        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('notificationUpdate', kwargs = {'pk': notification.pk, 'notification_type': 'game' })
        response = self.client.put(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(NotificationFriend.objects.get(pk = notification.pk).active)
        self.assertEqual(NotificationFriend.objects.all().count(), 1)

    def test_update_notification_404_NOT_FOUND_C(self):
        """ 
            Fede tries to update Nico's Friend Notification
        """
        fede = PlayerFactory()
        nico = PlayerFactory()
        notification = NotificationFriendFactory(player = nico, sender = fede)
        self.assertTrue(NotificationFriend.objects.get(pk = notification.pk).active)

        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('notificationUpdate', kwargs = {'pk': notification.pk, 'notification_type': 'friend' })
        response = self.client.put(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(NotificationFriend.objects.get(pk = notification.pk).active)
        self.assertEqual(NotificationFriend.objects.all().count(), 1)

    def test_update_notification_404_NOT_FOUND_D(self):
        """ 
            Fede tries to update Nico's Game Notification
        """
        fede = PlayerFactory()
        nico = PlayerFactory()
        notification = NotificationGameFactory(player = nico, sender = fede)
        self.assertTrue(NotificationGame.objects.get(pk = notification.pk).active)

        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('notificationUpdate', kwargs = {'pk': notification.pk, 'notification_type': 'game' })
        response = self.client.put(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(NotificationGame.objects.get(pk = notification.pk).active)
        self.assertEqual(NotificationGame.objects.all().count(), 1)

    def test_update_401_UNAUTHORIZED(self):
        """ 
            Anon tries to update Nico Notification
        """
        nico = PlayerFactory()
        notification = NotificationFriendFactory(player = nico)
        self.assertTrue(NotificationFriend.objects.get(pk = notification.pk).active)

        url = reverse('notificationUpdate', kwargs = {'pk': notification.pk, 'notification_type': 'friend' })
        response = self.client.put(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(NotificationFriend.objects.get(pk = notification.pk).active)
        self.assertEqual(NotificationFriend.objects.all().count(), 1)

