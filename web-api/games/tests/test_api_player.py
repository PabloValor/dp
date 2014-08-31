import json
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from ..serializers import GameSerializer
from ..factories import *

class PlayerAPITest(APITestCase):
    def test_create_200_OK(self): 
        data = { 'username': 'nico',
                 'email': 'nmbases@gmail.com',
                 'password': 'nicolas1' }

        url = reverse('playerCreate')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.all().count(), 1)

    def test_create_username_duplicated_400_BAD_REQUEST(self): 
        player = PlayerFactory()
        data = { 'username': player.username,
                 'email': 'nmbases@gmail.com',
                 'password': 'nico' }

        url = reverse('playerCreate')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Player.objects.all().count(), 1)
        self.assertTrue(response.data.has_key('username'))

    def test_create_without_username_400_BAD_REQUEST(self): 
        data = { 'username': '',
                 'email': 'nmbases@gmail.com',
                 'password': 'nico' }

        url = reverse('playerCreate')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Player.objects.all().count(), 0)
        self.assertTrue(response.data.has_key('username'))

    def test_create_without_password_400_BAD_REQUEST(self): 
        data = { 'username': 'nico',
                 'email': 'nmbases@gmail.com',
                 'password': '' }

        url = reverse('playerCreate')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Player.objects.all().count(), 0)
        self.assertTrue(response.data.has_key('password'))

    def test_create_username_duplicated_400_BAD_REQUEST(self): 
        player = PlayerFactory()
        data = { 'username': player.username,
                 'email': 'nmbases@gmail.com',
                 'password': 'nicolas1' }

        url = reverse('playerCreate')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Player.objects.all().count(), 1)
        self.assertTrue(response.data.has_key('username'))

    def test_update_user_401_UNAUTHORIZED(self):
        game = GameFactory()
        player = PlayerFactory()
        data = { 'games': [game.pk] }

        url = reverse('playerUpdate', kwargs = { 'pk': player.pk })
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_other_user_401_UNAUTHORIZED(self):
        player = PlayerFactory()
        player_2 = PlayerFactory()

        game = GameFactory()
        data = { 'games': [game.pk] }

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player tries to update Player 2 
        url = reverse('playerUpdate', kwargs = { 'pk': player_2.pk })
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_200_OK(self):
        player = PlayerFactory()
        game = GameFactory()

        data = { 'games': [game.pk] }

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerUpdate', kwargs = { 'pk': player.pk })
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # TODO: cambiar para que se actualice bien el usuario con otors datos y no con el juego
        #player_game = Player.objects.get(pk = player.pk).games.all()[0]
        #self.assertEqual(player_game.pk, game.pk)

    def test_update_user_forbidden_values_200_OK(self):
        player = PlayerFactory()
        game = GameFactory()

        data = { 'games': [game.pk], 
                'username': 'nico',
                'email': 'nico@email.com'}

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerUpdate', kwargs = { 'pk': player.pk })
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        player_db = Player.objects.get(pk = player.pk)
        self.assertEqual(player_db.username, player.username)
        self.assertEqual(player_db.email, player.email)


    def test_get_list_of_players_200_OK(self): 
        player = PlayerFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerList')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_of_players_401_UNAUTHORIZED(self): 
        player = PlayerFactory()

        url = reverse('playerList')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_player_200_OK(self): 
        player = PlayerFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerDetail', kwargs = {'pk': player.pk })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_player_401_UNAUTHORIZED(self): 
        player = PlayerFactory()

        url = reverse('playerDetail', kwargs = {'pk': player.pk })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_player_with_notification_after_login_200_OK_A(self): 
        """ 
          Test if the player recevies the notifications after he logs in the site
        """

        data = { 'username': 'nico',
                 'email': 'nmbases@gmail.com',
                 'password': 'nicolas1' }

        url = reverse('playerCreate')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('loginToken')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.has_key('game_notifications'))
        self.assertTrue(response.data.has_key('friend_notifications'))

    def test_get_player_with_notification_after_login_200_OK_B(self): 
        """ 
          Test if the player recevies the notifications after he logs in the site

          Player is invited to a game 
        """

        # Register a new player: we need to know the password so we use this technique
        data = { 'username': 'nico',
                 'email': 'nmbases@gmail.com',
                 'password': 'nicolas1' }

        url = reverse('playerCreate')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        player = Player.objects.first()

        # New Game
        game = GameFactory()

        # The player is invited
        GamePlayerFactory(game = game, player = player)

        # Login
        url = reverse('loginToken')
        response = self.client.post(url, data)
        import ipdb; ipdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['game_notifications']), 1)
        self.assertEqual(response.data['game_notifications'][0]['player']['id'], player.id)



class PlayerSearchAPITest(APITestCase):
    def test_get_all__401_UNAUTHORIZED(self): 
        player = PlayerFactory()

        url = reverse('playerListSearch', kwargs={'username': ''})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_filter_current_user_200_OK(self): 
        player = PlayerFactory()

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerListSearch', kwargs={'username': player.username})
        response = self.client.get(url)

        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_returns_nothing_200_OK(self): 
        player = PlayerFactory()
        player_2 = PlayerFactory()

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerListSearch', kwargs={'username': ''})
        response = self.client.get(url)

        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_search_ignore_case_200_OK(self): 
        player = PlayerFactory()
        PlayerFactory(username = 'User 1')
        PlayerFactory(username = 'UsEr 2')

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerListSearch', kwargs={'username': 'user'})
        response = self.client.get(url)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_search_ignore_whitespace_200_OK(self): 
        player = PlayerFactory()
        PlayerFactory(username = 'User 1')
        PlayerFactory(username = 'UsEr 2')

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerListSearch', kwargs={'username': ' user   '})
        response = self.client.get(url)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_filter_200_OK(self): 
        player = PlayerFactory()
        PlayerFactory(username = 'User 1')
        PlayerFactory(username = 'UsEr 2')
        PlayerFactory(username = 'Name 2')
        PlayerFactory(username = 'USERName 2')

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerListSearch', kwargs={'username': ' uSeR   '})
        response = self.client.get(url)

        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PlayerFriendAPITest(APITestCase):
    def test_post_make_friend_200_OK(self): 
        player = PlayerFactory()
        friend = PlayerFactory()

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerFriendCreate')
        response = self.client.post(url, {'friend': friend.id}, format='json')

        self.assertEqual(len(player.get_true_friends()), 0)
        self.assertEqual(len(player.get_all_friends()), 1)
        self.assertEqual(len(player.get_ignored_friends()), 0)
        self.assertEqual(len(player.get_friends_that_ignored_us()), 1)

        self.assertEqual(len(friend.get_true_friends()), 0)
        self.assertEqual(len(friend.get_all_friends()), 1)
        self.assertEqual(len(friend.get_ignored_friends()), 1)
        self.assertEqual(len(friend.get_friends_that_ignored_us()), 0)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_make_friend_duplicated_400_BAD_REQUEST(self):
        player = PlayerFactory()
        friend = PlayerFactory()
        PlayerFriendFactory(player = player, friend = friend)

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerFriendCreate')
        response = self.client.post(url, {'friend': friend.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_make_friend_duplicated_reversed_400_BAD_REQUEST(self):
        # Now we try to create a new friendship with a guy that has already 
        # sent us an invitacion
        player = PlayerFactory()
        friend = PlayerFactory()
        PlayerFriendFactory(player = player, friend = friend)

        # Player authentication
        token = Token.objects.get(user__username = friend.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerFriendCreate')
        response = self.client.post(url, {'friend': player.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_player_friends_A_200_OK(self): 
        player = PlayerFactory()
        pf_1 = PlayerFriendFactory(player = player)
        pf_2 = PlayerFriendFactory(player = player)

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerFriendsList')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], pf_1.friend.id)
        self.assertEqual(response.data[1]['id'], pf_2.friend.id)

        self.assertEqual(len(player.get_friends_that_ignored_us()), 2)
        self.assertEqual(len(player.get_true_friends()), 0)
        self.assertEqual(len(player.get_all_friends()), 2)
        self.assertEqual(len(player.get_ignored_friends()), 0)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_player_friends_B_200_OK(self): 
        # Now me test the other way around
        player = PlayerFactory()
        pf_1 = PlayerFriendFactory(player = player)
        pf_2 = PlayerFriendFactory(player = player)

        # Friend 1 authentication
        token = Token.objects.get(user__username = pf_1.friend.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerFriendsList')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], player.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Friend 2 authentication
        token = Token.objects.get(user__username = pf_2.friend.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerFriendsList')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], player.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_player_limbo_friends_A_200_OK(self): 
        player = PlayerFactory()
        pf_1 = PlayerFriendFactory(player = player)
        pf_2 = PlayerFriendFactory(player = player)

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerFriendsList')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], pf_1.friend.id)
        self.assertTrue(response.data[0]['is_limbo_friend'])

        self.assertEqual(response.data[1]['id'], pf_2.friend.id)
        self.assertTrue(response.data[1]['is_limbo_friend'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_player_limbo_friends_B_200_OK(self): 
        player = PlayerFactory()
        pf_1 = PlayerFriendFactory(player = player)
        pf_2 = PlayerFriendFactory(player = player)

        # Player authentication
        token = Token.objects.get(user__username = pf_1.friend.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerFriendsList')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], player.id)
        self.assertFalse(response.data[0]['is_limbo_friend'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_friends_401_UNAUTHORIZED(self): 
        url = reverse('playerFriendsList')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_player_sends_another_invitation_400_BAD_REQUEST(self): 
        # Only the player that rejects the invitation can make a new one
        player = PlayerFactory()
        friend = PlayerFactory()
        pf = PlayerFriendFactory(player = player, friend = friend, status = False)

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerFriendCreate')
        response = self.client.post(url, {'friend': friend.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_player_sends_another_invitation_200_OK(self): 
        # Only the player that rejects the invitation can make a new one
        player = PlayerFactory()
        friend = PlayerFactory()
        pf = PlayerFriendFactory(player = player, friend = friend, status = False)

        # Player authentication
        token = Token.objects.get(user__username = friend.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        self.assertEqual(len(player.get_bad_friends()), 1)
        self.assertEqual(len(friend.get_friends_we_rejected()), 1)

        url = reverse('playerFriendCreate')
        response = self.client.post(url, {'friend': player.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(player.get_bad_friends()), 0)
        self.assertEqual(len(player.get_ignored_friends()), 1)
        self.assertEqual(len(friend.get_friends_we_rejected()), 0)

    def test_update_player_rejects_invitation_200_OK(self): 
        player = PlayerFactory()
        PlayerFactory()
        friend = PlayerFactory()
        pf = PlayerFriendFactory(player = player, friend = friend)

        # Player authentication
        token = Token.objects.get(user__username = friend.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        self.assertEqual(len(player.get_true_friends()), 0)
        self.assertEqual(len(player.get_bad_friends()), 0)
        self.assertEqual(len(friend.get_true_friends()), 0)
        self.assertEqual(len(friend.get_ignored_friends()), 1)
        self.assertEqual(len(friend.get_friends_we_rejected()), 0)

        url = reverse('playerFriendUpdate', kwargs={'pk': player.id})
        response = self.client.put(url, {'status': False }, format='json')

        self.assertEqual(len(player.get_true_friends()), 0)
        self.assertEqual(len(player.get_bad_friends()), 1)
        self.assertEqual(len(friend.get_true_friends()), 0)
        self.assertEqual(len(friend.get_ignored_friends()), 0)
        self.assertEqual(len(friend.get_friends_we_rejected()), 1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_player_rejects_invitation_200_OK(self): 
        player = PlayerFactory()
        PlayerFactory()
        friend = PlayerFactory()
        pf = PlayerFriendFactory(player = player, friend = friend)

        # Player authentication
        token = Token.objects.get(user__username = friend.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        self.assertEqual(len(player.get_true_friends()), 0)
        self.assertEqual(len(player.get_bad_friends()), 0)
        self.assertEqual(len(friend.get_true_friends()), 0)
        self.assertEqual(len(friend.get_ignored_friends()), 1)
        self.assertEqual(len(friend.get_friends_we_rejected()), 0)

        url = reverse('playerFriendUpdate', kwargs={'pk': player.id})
        response = self.client.put(url, {'status': False }, format='json')

        self.assertEqual(len(player.get_true_friends()), 0)
        self.assertEqual(len(player.get_bad_friends()), 1)
        self.assertEqual(len(friend.get_true_friends()), 0)
        self.assertEqual(len(friend.get_ignored_friends()), 0)
        self.assertEqual(len(friend.get_friends_we_rejected()), 1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_player_tries_to_cheat_invitation_A_400_BAD_REQUEST(self): 
        player = PlayerFactory()
        friend = PlayerFactory()
        pf = PlayerFriendFactory(player = player, friend = friend)

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerFriendUpdate', kwargs={'pk': player.id})
        response = self.client.put(url, {'status': False }, format='json')

        self.assertEqual(len(player.get_true_friends()), 0)
        self.assertEqual(len(friend.get_true_friends()), 0)
        self.assertEqual(len(friend.get_ignored_friends()), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('playerFriendUpdate', kwargs={'pk': friend.id})
        response = self.client.put(url, {'status': True }, format='json')

        self.assertEqual(len(player.get_true_friends()), 0)
        self.assertEqual(len(friend.get_true_friends()), 0)
        self.assertEqual(len(friend.get_ignored_friends()), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_player_tries_to_cheat_invitation_B_400_BAD_REQUEST(self): 
        # A completely different user tries to cheat it
        player = PlayerFactory()
        pf = PlayerFriendFactory()

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerFriendUpdate', kwargs={'pk': pf.player.id})
        response = self.client.put(url, {'status': True }, format='json')

        url = reverse('playerFriendUpdate', kwargs={'pk': pf.friend.id})
        response = self.client.put(url, {'status': True }, format='json')

        self.assertEqual(len(pf.player.get_true_friends()), 0)
        self.assertEqual(len(pf.friend.get_true_friends()), 0)
        self.assertEqual(len(pf.friend.get_ignored_friends()), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_player_tries_to_cheat_invitation_C_400_BAD_REQUEST(self): 
        # A user with a relantionship tries to cheat other one
        player = PlayerFactory()
        friend = PlayerFactory()
        PlayerFriendFactory(player = player, friend = friend)
        pf = PlayerFriendFactory(friend = friend)

        # Player authentication
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerFriendUpdate', kwargs={'pk': friend.id})
        response = self.client.put(url, {'status': True }, format='json')

        url = reverse('playerFriendUpdate', kwargs={'pk': player.id})
        response = self.client.put(url, {'status': True }, format='json')

        self.assertEqual(len(pf.friend.get_true_friends()), 0)
        self.assertEqual(len(pf.friend.get_ignored_friends()), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PlayerMatchPredictionAPITest(APITestCase):
    def test_nico_does_a_prediction_201_CREATED(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        self.assertEqual(gp.match_predictions.count(), 0)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionCreate')
        response = self.client.post(url, {'gameplayer': gp.id, 'match': match.id, 'visitor_team_goals': 1, 'local_team_goals': 2 }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(gp.match_predictions.count(), 1)
        self.assertEqual(gp.match_predictions.first().visitor_team_goals, 1)
        self.assertEqual(gp.match_predictions.first().local_team_goals, 2)

    def test_nico_does_a_prediction_of_a_finished_match_403_FORBIDDEN(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture, is_finished = True)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        self.assertEqual(gp.match_predictions.count(), 0)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionCreate')
        response = self.client.post(url, {'gameplayer': gp.id, 'match': match.id, 'visitor_team_goals': 1, 'local_team_goals': 2 }, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_nico_does_a_prediction_of_a_finished_fixture_403_FORBIDDEN(self):
        # Tournament
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        self.assertEqual(gp.match_predictions.count(), 0)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionCreate')
        response = self.client.post(url, {'gameplayer': gp.id, 'match': match.id, 'visitor_team_goals': 1, 'local_team_goals': 2 }, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_nico_does_a_prediction_of_an_unexisting_match_404_NOT_FOUND(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        self.assertEqual(gp.match_predictions.count(), 0)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionCreate')
        response = self.client.post(url, {'gameplayer': gp.id, 'match': match.id + 1, 'visitor_team_goals': 1, 'local_team_goals': 2 }, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_anon_try_to_do_a_prediction_401_UNAUTHORIZED(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        self.assertEqual(gp.match_predictions.count(), 0)

        # Anon makes request
        url = reverse('playerMatchPredictionCreate')
        response = self.client.post(url, {'gameplayer': gp.id, 'match': match.id, 'visitor_team_goals': 1, 'local_team_goals': 2 }, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_fede_tries_to_do_a_prediction_as_nico_403_FORBIDDEN(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)

        # Fede
        fede = PlayerFactory()
        gp_1 = GamePlayerFactory(game = game, player = fede, status = True)

        # Fede authentication
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionCreate')
        response = self.client.post(url, {'gameplayer': gp.id, 'match': match.id, 'visitor_team_goals': 1, 'local_team_goals': 2 }, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_nico_does_two_predictions_for_the_same_match_the_first_one_is_deleted_201_CREATED(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico does a prediction
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match)
        self.assertEqual(gp.match_predictions.count(), 1)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionCreate')
        response = self.client.post(url, {'gameplayer': gp.id, 'match': match.id, 'visitor_team_goals': 1, 'local_team_goals': 2 }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(gp.match_predictions.count(), 1)

    def test_nico_does_two_predictions_for_the_same_match_but_different_game_201_CREATED(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico does a prediction
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match)
        self.assertEqual(gp.match_predictions.count(), 1)

        # Nico does a second prediction in another game
        game_2 = GameFactory(tournament = fixture.tournament)
        gp_2 = GamePlayerFactory(game = game_2, player = nico, status = True)

        # Nico authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionCreate')
        response = self.client.post(url, {'gameplayer': gp_2.id, 'match': match.id, 'visitor_team_goals': 1, 'local_team_goals': 2 }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(gp.match_predictions.count(), 1)
        self.assertEqual(gp_2.match_predictions.count(), 1)

    def test_nico_does_a_prediction_of_a_game_that_he_isnt_playing_403_FORBIDDEN_A(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = False)
        self.assertEqual(gp.match_predictions.count(), 0)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionCreate')
        response = self.client.post(url, {'gameplayer': gp.id, 'match': match.id, 'visitor_team_goals': 1, 'local_team_goals': 2 }, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_nico_does_a_prediction_of_a_game_that_he_isnt_playing_403_FORBIDDEN_B(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = None)
        self.assertEqual(gp.match_predictions.count(), 0)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionCreate')
        response = self.client.post(url, {'gameplayer': gp.id, 'match': match.id, 'visitor_team_goals': 1, 'local_team_goals': 2 }, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_nico_does_a_prediction_of_a_fixture_already_closed_403_FORBIDDEN(self):
        # Tournament
        fixture = FixtureFactory(open_until = datetime.now())
        match = MatchFactory(fixture = fixture)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        self.assertEqual(gp.match_predictions.count(), 0)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionCreate')
        response = self.client.post(url, {'gameplayer': gp.id, 'match': match.id, 'visitor_team_goals': 1, 'local_team_goals': 2 }, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_nico_gets_his_prediction_of_a_game_200_OK_A(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_nico_gets_his_prediction_of_a_game_200_OK_B(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico is playing two games and does two predictions of the same match
        nico = PlayerFactory()

        # Game 1
        game = GameFactory(tournament = fixture.tournament)
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match)

        # Game 2
        game_2 = GameFactory(tournament = fixture.tournament)
        gp_2 = GamePlayerFactory(game = game_2, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp_2, match = match)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Gets Game 1 predictions
        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Gets Game 2 predictions
        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_nico_gets_his_multiple_predictions_of_a_game_200_OK_A(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)
        match_2 = MatchFactory(fixture = fixture)
        match_3 = MatchFactory(fixture = fixture)

        # Nico is playing two games and does two predictions of the same match
        nico = PlayerFactory()

        # Game 1
        game = GameFactory(tournament = fixture.tournament)
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_2)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_3)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Gets Game 1 predictions
        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_nico_gets_his_multiple_predictions_of_a_game_200_OK_B(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)
        match_2 = MatchFactory(fixture = fixture)
        match_3 = MatchFactory(fixture = fixture)

        # Nico is playing two games and does two predictions of the same match
        nico = PlayerFactory()

        # Game 1
        game = GameFactory(tournament = fixture.tournament)
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_2)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_3)

        # Game 2
        game_2 = GameFactory(tournament = fixture.tournament)
        gp_2 = GamePlayerFactory(game = game_2, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp_2, match = match)
        PlayerMatchPredictionFactory(gameplayer = gp_2, match = match_3)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Gets Game 1 predictions
        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        # Gets Game 2 predictions
        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_nico_gets_his_predictions_sorted_by_fixture_number_200_OK_A(self):
        # Tournament 
        tournament = TournamentFactory()

        # Fixtures
        fixture_1 = FixtureFactory(tournament = tournament, number = 1)
        match_1 = MatchFactory(fixture = fixture_1)
        fixture_2 = FixtureFactory(tournament = tournament, number = 2)
        match_2 = MatchFactory(fixture = fixture_2)

        # Nico
        game = GameFactory(tournament = tournament)
        nico = PlayerFactory()

        # Predictions
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_1)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_2)

        # Nico authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['match']['id'] , match_1.id)
        self.assertEqual(response.data[1]['match']['id'], match_2.id)

    def test_nico_gets_his_predictions_sorted_by_fixture_number_200_OK_B(self):
        # Tournament 
        tournament = TournamentFactory()

        # Fixtures
        fixture_1 = FixtureFactory(tournament = tournament, number = 2)
        match_1 = MatchFactory(fixture = fixture_1)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        match_2 = MatchFactory(fixture = fixture_2)

        # Nico
        game = GameFactory(tournament = tournament)
        nico = PlayerFactory()

        # Predictions
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_1)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_2)

        # Nico authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['match']['id'] , match_2.id)
        self.assertEqual(response.data[1]['match']['id'] , match_1.id)

    def test_nico_gets_his_predictions_sorted_by_fixture_number_200_OK_C(self):
        # Tournament 
        tournament = TournamentFactory()

        # Fixtures
        fixture_1 = FixtureFactory(tournament = tournament, number = 2)
        match_1 = MatchFactory(fixture = fixture_1)
        match_2 = MatchFactory(fixture = fixture_1)
        match_3 = MatchFactory(fixture = fixture_1)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        match_4 = MatchFactory(fixture = fixture_2)
        match_5 = MatchFactory(fixture = fixture_2)

        # Nico
        game = GameFactory(tournament = tournament)
        nico = PlayerFactory()

        # Predictions
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_1)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_2)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_3)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_4)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match_5)

        # Nico authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]['match']['id'] , match_4.id)
        self.assertEqual(response.data[1]['match']['id'] , match_5.id)
        self.assertEqual(response.data[2]['match']['id'] , match_1.id)

    def test_nico_gets_his_prediction_with_match_detailed_200_OK(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match)

        # Player authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['match']['fixture'] , fixture.id)

    def test_nico_gets_his_prediction_with_points_classic_game_200_OK_A(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture, visitor_team_goals = 1, local_team_goals = 1, is_finished = True)

        # Nico
        game = GameFactory(tournament = fixture.tournament, classic = True)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match, visitor_team_goals = 1, local_team_goals = 1)

        # Nico authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['points'], 3)

    def test_nico_gets_his_prediction_with_points_classic_game_200_OK_B(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture, visitor_team_goals = 1, local_team_goals = 1, is_finished = True)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match, visitor_team_goals = 0, local_team_goals = 1)

        # Nico authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['points'], 0)

    def test_nico_gets_his_prediction_with_points_classic_game_200_OK_C(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture, visitor_team_goals = 1, local_team_goals = 1, is_finished = False)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match, visitor_team_goals = 0, local_team_goals = 1)

        # Nico authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['points'], None)

    def test_anon_tries_to_get_nicos_predictions_401_UNAUTHORIZED(self):
        """
          Anon tries to get Nico's predictions
        """
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico
        game = GameFactory(tournament = fixture.tournament)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match)


        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fede_get_nico_gets_predictions_200_OK(self):
        """
          Fede gets Nico's predictions 
        """
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture, visitor_team_goals = 1, local_team_goals = 1, is_finished = False)
        game = GameFactory(tournament = fixture.tournament)

        # Nico
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match, visitor_team_goals = 0, local_team_goals = 1)

        # Fede
        fede = PlayerFactory()
        GamePlayerFactory(game = game, player = fede, status = True)

        # Fede authentication
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_fede_get_nico_gets_predictions_403_FORBIDDEN_A(self):
        """
          Fede tries to get Nico's predictions but Fede doesn't play this game
        """
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture, visitor_team_goals = 1, local_team_goals = 1, is_finished = False)

        # Nico
        nico = PlayerFactory()
        game = GameFactory(tournament = fixture.tournament)
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match, visitor_team_goals = 0, local_team_goals = 1)

        # Fede
        fede = PlayerFactory()
        game_2 = GameFactory(tournament = fixture.tournament)
        GamePlayerFactory(game = game_2, player = fede, status = True)

        # Fede authentication
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fede_get_nico_gets_predictions_403_FORBIDDEN_B(self):
        """
          Fede tries to get Nico's predictions but Fede didn't answer the Game Request
        """
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture, visitor_team_goals = 1, local_team_goals = 1, is_finished = False)

        # Nico
        nico = PlayerFactory()
        game = GameFactory(tournament = fixture.tournament)
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match, visitor_team_goals = 0, local_team_goals = 1)

        # Fede
        fede = PlayerFactory()
        GamePlayerFactory(game = game, player = fede, status = None)

        # Fede authentication
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fede_get_nico_gets_predictions_403_FORBIDDEN_C(self):
        """
          Fede tries to get Nico's predictions but Fede rejected playing the game
        """
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture, visitor_team_goals = 1, local_team_goals = 1, is_finished = False)

        # Nico
        nico = PlayerFactory()
        game = GameFactory(tournament = fixture.tournament)
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match, visitor_team_goals = 0, local_team_goals = 1)

        # Fede
        fede = PlayerFactory()
        GamePlayerFactory(game = game, player = fede, status = False)

        # Fede authentication
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fede_get_nico_gets_predictions_403_FORBIDDEN_D(self):
        """
          Fede tries to get Nico's predictions but the Game doesn't allow that
        """
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture, visitor_team_goals = 1, local_team_goals = 1, is_finished = False)

        # Nico
        nico = PlayerFactory()
        game = GameFactory(tournament = fixture.tournament, open_predictions = False)
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match, visitor_team_goals = 0, local_team_goals = 1)

        # Fede
        fede = PlayerFactory()
        GamePlayerFactory(game = game, player = fede, status = True)

        # Fede authentication
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_nico_gets_his_prediction_in_a_closed_prediction_game_200_OK(self):
        # Tournament
        fixture = FixtureFactory()
        match = MatchFactory(fixture = fixture)

        # Nico
        game = GameFactory(tournament = fixture.tournament, open_predictions = False)
        nico = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = nico, status = True)
        PlayerMatchPredictionFactory(gameplayer = gp, match = match, visitor_team_goals = 0, local_team_goals = 1)

        # Nico authentication
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('playerMatchPredictionList', kwargs = {'gp': gp.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
