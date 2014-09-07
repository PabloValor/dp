import json
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from ..serializers import GameSerializer
from ..factories import *

class GameAPITest(APITestCase):
    def test_get_200_OK(self):
        player = PlayerFactory()
        game_1 = GamePlayerFactory(player = player)
        game_2 = GamePlayerFactory(player = player)

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameList')
        response = self.client.get(url)
        r_games = json.loads(response.content)

        self.assertEqual(r_games[0]['name'], game_1.game.name)
        self.assertEqual(r_games[1]['name'], game_2.game.name)
        self.assertTrue(r_games[1]['open_predictions'])
        self.assertEqual(len(r_games), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_404_NOT_FOUND(self):
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameDetail', kwargs = {'pk': 1 })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_201_CREATED(self):
        player = PlayerFactory()
        tournament = TournamentFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers': [{'player': player.id, 'username': player.username}] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.first().owner, player)
        self.assertTrue(Game.objects.first().classic)
        self.assertTrue(player.gameplayer_set.first().status)

        # Default points
        self.assertEqual(Game.objects.first().points_exact, 3)
        self.assertEqual(Game.objects.first().points_general, 3)
        self.assertEqual(Game.objects.first().points_classic, 2)
        self.assertEqual(Game.objects.first().points_double, 2)

    def test_create_with_custom_points_201_CREATED(self):
        player = PlayerFactory()
        tournament = TournamentFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 
                 'tournament': tournament.pk, 
                 'points_exact': 5, 
                 'points_general': 4, 
                 'points_classic': 3, 
                 'points_double': 1, 
                 'gameplayers': [{'player': player.id, 'username': player.username}] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.first().owner, player)
        self.assertTrue(Game.objects.first().classic)
        self.assertTrue(player.gameplayer_set.first().status)

        # Default points
        self.assertEqual(Game.objects.first().points_exact, 5)
        self.assertEqual(Game.objects.first().points_general, 4)
        self.assertEqual(Game.objects.first().points_classic, 3)
        self.assertEqual(Game.objects.first().points_double, 1)

    def test_create_with_invalid_custom_points_400_BAD_REQUEST(self):
        player = PlayerFactory()
        tournament = TournamentFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 
                 'tournament': tournament.pk, 
                 'points_exact': 5, 
                 'points_general': -4,  # Invalid
                 'points_classic': 3, 
                 'points_double': 1, 
                 'gameplayers': [{'player': player.id, 'username': player.username}] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_game_not_classic_201_CREATED(self):
        player = PlayerFactory()
        tournament = TournamentFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers': [{'player': player.id, 'username': player.username}], 'classic': False }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.first().owner, player)
        self.assertTrue(player.gameplayer_set.first().status)
        self.assertFalse(Game.objects.first().classic)

    def test_create_401_UNAUTHORIZED(self):
        player = PlayerFactory()
        tournament = TournamentFactory()

        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_get_200_OK(self):
        player = PlayerFactory()
        tournament = TournamentFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Create two games
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers': [{'player': player.id, 'username': player.username}] }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = { 'name' : 'Game 2', 'tournament': tournament.pk, 'gameplayers': [{'player': player.id, 'username': player.username}] }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get Games
        url = reverse('gameList')
        response = self.client.get(url)
        games = json.loads(response.content)
        self.assertEqual(len(games), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_200_OK(self):
        game = GameFactory()
        owner = game.owner

        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameDetail', kwargs = {'pk': game.pk })

        game.name = 'New Game'
        serializer = GameSerializer(game)
        response = self.client.put(url, serializer.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_401_UNAUTHORIZED(self):
        game = GameFactory()

        url = reverse('gameDetail', kwargs = {'pk': game.pk })

        serializer = GameSerializer(game)
        response = self.client.put(url, serializer.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_403_FORBIDDEN(self):
        player = PlayerFactory()
        game = GameFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameDetail', kwargs = {'pk': game.pk })

        serializer = GameSerializer(game)
        response = self.client.put(url, serializer.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_201_CREATED(self):
        game = GameFactory()
        owner = game.owner

        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameDetail', kwargs = {'pk': game.pk + 1 })

        serializer = GameSerializer(game)
        response = self.client.put(url, serializer.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_get_200_OK(self):
        game = GameFactory()
        owner = game.owner

        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameDetail', kwargs = {'pk': game.pk })

        # Update
        name = 'New Game'
        game.name = name
        serializer = GameSerializer(game)
        response = self.client.put(url, serializer.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get
        response = self.client.get(url)
        game = json.loads(response.content)
        self.assertEqual(game['name'], name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_get_update_200_OK(self):
        player = PlayerFactory()
        tournament = TournamentFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Create 
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers': [{'player': player.id, 'username': player.username}] }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get
        url = reverse('gameList')
        response = self.client.get(url)
        games = json.loads(response.content)
        self.assertEqual(len(games), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update
        game = games[0]
        url = reverse('gameDetail', kwargs = {'pk': game['id'] })
        game['name'] = 'Game 2'
        response = self.client.put(url, game, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_200_OK(self):
        game = GameFactory()
        owner = game.owner

        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameDetail', kwargs = {'pk': game.pk })

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Game.objects.all().count(), 0)

    def test_delete_403_FORBIDDEN(self):
        game = GameFactory()
        player = PlayerFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameDetail', kwargs = {'pk': game.pk })

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_401_UNAUTHORIZED(self):
        game = GameFactory()

        url = reverse('gameDetail', kwargs = {'pk': game.pk })

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_with_one_players_200_OK(self):
        # The owner is a player
        owner = PlayerFactory()
        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        player = PlayerFactory()
        PlayerFriendFactory(player = owner, friend = player, status = True)
        tournament = TournamentFactory()

        # Create 
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers' : [{'player':owner.id, 'username': owner.username}, {'player':player.id, 'username': player.username}] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.all()[0].players.count(), 2)
        self.assertEqual(Game.objects.all()[0].owner, owner)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_with_one_player_that_are_not_friends_400_BAD_REQUEST_A(self):
        # The owner is a player
        owner = PlayerFactory()
        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        player = PlayerFactory()
        tournament = TournamentFactory()

        # Create 
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers' : [{'player':player.id, 'username': player.username}] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(Game.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_one_player_that_are_not_friends_400_BAD_REQUEST_B(self):
        # The owner is a player
        owner = PlayerFactory()
        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        player = PlayerFactory()
        PlayerFriendFactory(player = owner, friend = player, status = None)
        tournament = TournamentFactory()

        # Create 
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers' : [{'player':player.id, 'username': player.username}] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(Game.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_one_player_that_are_not_friends_400_BAD_REQUEST_C(self):
        # The owner is a player
        owner = PlayerFactory()
        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        player = PlayerFactory()
        PlayerFriendFactory(player = owner, friend = player, status = False)
        tournament = TournamentFactory()

        # Create 
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers' : [{'player':player.id, 'username': player.username}] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(Game.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_two_players_201_CREATED(self):
        # The owner is a player
        owner = PlayerFactory()
        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        player = PlayerFactory()
        PlayerFriendFactory(player = owner, friend = player, status = True)
        player_2 = PlayerFactory()
        PlayerFriendFactory(player = player_2, friend = owner, status = True)
        tournament = TournamentFactory()

        # Create 
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers' : [{'player':player.id, 'username': player.username}, {'player':player_2.id, 'username': player_2.username }, {'player':owner.id, 'username': owner.username}] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.all()[0].players.count(), 3)
        self.assertEqual(Game.objects.all()[0].owner, owner)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_with_two_players_that_one_is_not_friend_400_BAD_REQUEST(self):
        # The owner is a player
        owner = PlayerFactory()
        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        player = PlayerFactory()
        PlayerFriendFactory(player = owner, friend = player, status = True)
        player_2 = PlayerFactory()
        tournament = TournamentFactory()

        # Create 
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers' : [{'player':player.id, 'username': player.username}, {'player':player_2.id, 'username': player_2.username}] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(Game.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_two_players_with_a_non_existing_player_400_BAD_REQUEST(self):
        # The owner is a player
        owner = PlayerFactory()
        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        player = PlayerFactory()
        PlayerFriendFactory(player = owner, friend = player, status = True)
        tournament = TournamentFactory()

        # Create 
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers' : [{'player':player.id, 'username': player.username}, {'player': 99, 'username': player.username}] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(Game.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_two_players_with_a_duplicate_player_400_BAD_REQUEST(self):
        # The owner is a player
        owner = PlayerFactory()
        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        player = PlayerFactory()
        PlayerFriendFactory(player = owner, friend = player, status = True)
        tournament = TournamentFactory()

        # Create 
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers' : [{'player':player.id, 'username': player.username}, {'player': player.id, 'username': player.username}] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(Game.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nico_creates_a_game_with_open_predictions_201_CREATED(self):
        nico = PlayerFactory()
        tournament = TournamentFactory()

        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers': [{'player': nico.id, 'username': nico.username}]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Game.objects.first().open_predictions)

    def test_nico_creates_a_game_with_closed_predictions_201_CREATED(self):
        nico = PlayerFactory()
        tournament = TournamentFactory()

        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers': [{'player': nico.id, 'username': nico.username}], 'open_predictions': False}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(Game.objects.first().open_predictions)

class GameAPIInvitationTest(APITestCase):
    """ 
      PLAYER ACCEPTS OR REJECTS GAME INVITATION

      The player who was invited decides if he is going to play the tournament or not 
    """
    def test_player_accepts_to_play_200_OK(self):
        # Player creates game
        owner = PlayerFactory()
        game = GameFactory(owner = owner)

        # Player invites a guy
        gp = GamePlayerFactory(game = game)
        guy = gp.player

        # Guy authenticates
        token = Token.objects.get(user__username = guy.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Guy accepts to play
        url = reverse('gamePlayerUpdate', kwargs = {'pk': gp.id })
        data = { 'status' : True  } 
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(GamePlayer.objects.get(pk = gp.pk).status)
              
    def test_player_rejects_to_play_200_OK(self):
        # Player creates game
        owner = PlayerFactory()
        game = GameFactory(owner = owner)

        # Player invites a guy
        gp = GamePlayerFactory(game = game)
        guy = gp.player

        # Guy authenticates
        token = Token.objects.get(user__username = guy.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Guy rejects to play
        url = reverse('gamePlayerUpdate', kwargs = {'pk': gp.id })
        data = { 'status' : False  } 
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(GamePlayer.objects.get(pk = gp.pk).status)

    def test_another_player_tries_to_update_the_game_player_for_him_400_BAD_REQUEST(self):
        # Player creates game
        owner = PlayerFactory()
        game = GameFactory(owner = owner)

        # Player invites a guy
        gp = GamePlayerFactory(game = game)

        # Player authenticates
        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # The Owner tries to update the GamePlayer Status
        url = reverse('gamePlayerUpdate', kwargs = {'pk': gp.id })
        data = { 'status' : True  } 
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(GamePlayer.objects.get(pk = gp.pk).status)

    def test_some_guy_tries_to_update_the_game_player_for_him_401_UNAUTHORIZED(self):
        # Player creates game
        owner = PlayerFactory()
        game = GameFactory(owner = owner)
        gp = GamePlayerFactory(game = game)

        # Some Guy tries to update the GamePlayer Status
        url = reverse('gamePlayerUpdate', kwargs = {'pk': gp.id })
        data = { 'status' : True  } 
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    """ 
        PLAYER REQUESTS FOR ANOTHER INVITATION AFTER HE REJECTED THE FIRST ONE

        When the player rejects to play he can request another invitation.
        If AnotherChance is None he can request another.
        If AnotherChance is False the player doesn't have any interest in play in this tournament.
        If AnotherChance is True the player he is requesting another chance to play.
    """

    def test_fede_who_rejected_to_play_ask_for_another_opportunity_200_OK(self):
        # Player creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede rejects invitation
        fede = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = fede, status = False)

        # Fede authenticates
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Fede asks for another opportunity
        url = reverse('gamePlayerUpdateAnotherChance', kwargs = {'pk': gp.id })
        data = { 'another_chance' : True  } 
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(GamePlayer.objects.get(id = gp.id).another_chance)

    def test_fede_who_rejected_to_play_sets_another_chance_to_false_200_OK(self):
        # Player creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede rejects invitation
        fede = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = fede, status = False)

        # Fede authenticates
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Fede asks for another opportunity
        url = reverse('gamePlayerUpdateAnotherChance', kwargs = {'pk': gp.id })
        data = { 'another_chance' : False  } 
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(GamePlayer.objects.get(id = gp.id).another_chance)

    def test_nico_wants_change_fede_game_player_another_chance_status_400_BAD_REQUEST(self):
        # Player creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede rejects invitation
        fede = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = fede, status = False)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico wants to change Fede GamePlayer 
        url = reverse('gamePlayerUpdateAnotherChance', kwargs = {'pk': gp.id })
        data = { 'another_chance' : True  } 
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(GamePlayer.objects.get(id = gp.id).another_chance)

    def test_anon_wants_change_fede_game_player_another_chance_status_401_UNAUTHORIZED(self):
        # Player creates a game
        game = GameFactory()

        # Fede rejects invitation
        fede = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = fede, status = False)

        # Anon wants to change Fede GamePlayer 
        url = reverse('gamePlayerUpdateAnotherChance', kwargs = {'pk': gp.id })
        data = { 'another_chance' : True  } 
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fede_who_rejected_to_play_ask_for_another_opportunity_when_he_is_already_playing_400_BAD_REQUEST(self):
        # Player creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede rejects invitation
        fede = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = fede, status = True)

        # Fede authenticates
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Fede asks for another opportunity
        url = reverse('gamePlayerUpdateAnotherChance', kwargs = {'pk': gp.id })
        data = { 'another_chance' : True  } 
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fede_who_rejected_to_play_ask_for_another_opportunity_when_he_didnt_asnwer_the_request_400_BAD_REQUEST(self):
        # Player creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede rejects invitation
        fede = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = fede, status = None)

        # Fede authenticates
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Fede asks for another opportunity
        url = reverse('gamePlayerUpdateAnotherChance', kwargs = {'pk': gp.id })
        data = { 'another_chance' : True  } 
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nico_wants_to_fool_around_and_update_his_another_chance_status_400_BAD_REQUEST(self):
        # Player creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)
        gp = GamePlayerFactory(player = nico, game = game)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Fede asks for another opportunity
        url = reverse('gamePlayerUpdateAnotherChance', kwargs = {'pk': gp.id })
        data = { 'another_chance' : True  } 
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """ 
        GAME OWNER INVITES AGAIN THE USER THAT REJECTED PREVIOUSLY BUT ASKED A NEW CHANCE

        Nico invites Fede again after he requested another chance 
    """

    def test_nico_invites_fede_again_after_his_request_200_OK(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede asks for another invitation
        fede = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = fede, status = False, another_chance = True)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico invites Fede again
        url = reverse('gamePlayerUpdateInvitesAgain', kwargs = {'pk': gp.id })
        response = self.client.put(url, None, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(GamePlayer.objects.get(id = gp.id).another_chance == None)
        self.assertTrue(GamePlayer.objects.get(id = gp.id).status == None)

    def test_nico_invites_fede_again_after_his_rejection_A_400_BAD_REQUEST(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede asks for another invitation
        fede = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = fede, status = False, another_chance = False)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico invites Fede again
        url = reverse('gamePlayerUpdateInvitesAgain', kwargs = {'pk': gp.id })
        response = self.client.put(url, None, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nico_invites_fede_again_after_his_rejection_B_400_BAD_REQUEST(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede asks for another invitation
        fede = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = fede, status = False, another_chance = None)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico invites Fede again
        url = reverse('gamePlayerUpdateInvitesAgain', kwargs = {'pk': gp.id })
        response = self.client.put(url, None, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fede_invites_fede_again_after_his_rejection_400_BAD_REQUEST(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede asks for another invitation
        fede = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = fede, status = False, another_chance = True)

        # Fede authenticates
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Fede invites Fede again
        url = reverse('gamePlayerUpdateInvitesAgain', kwargs = {'pk': gp.id })
        response = self.client.put(url, None, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anon_invites_fede_again_after_his_rejection_400_BAD_REQUEST(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede asks for another invitation
        fede = PlayerFactory()
        gp = GamePlayerFactory(game = game, player = fede, status = False, another_chance = True)

        # Anon invites Fede again
        url = reverse('gamePlayerUpdateInvitesAgain', kwargs = {'pk': gp.id })
        response = self.client.put(url, None, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    """ 
        GAME OWNER INVITES PLAYER AFTER THE CREATION OF THE GAME

        After creation of the game the Owner invites more players
    """

    def test_nico_invites_fede_after_game_creation(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico invites Fede to play
        fede = PlayerFactory()
        PlayerFriendFactory(player = fede, friend = nico, status = True)

        self.assertEqual(len(fede.games.all()), 0)
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(fede.games.all()), 1)

    def test_nico_invites_fede_after_game_creation_with_initial_points_201_CREATED(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico invites Fede to play
        fede = PlayerFactory()
        PlayerFriendFactory(player = fede, friend = nico, status = True)

        self.assertEqual(len(fede.games.all()), 0)
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id, 'initial_points': 10 }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(fede.games.all()), 1)
        self.assertEqual(fede.gameplayer_set.first().initial_points, 10)

    def test_nico_invites_fede_after_game_creation_with_invalid_initial_points_400_BAD_REQUEST(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico invites Fede to play
        fede = PlayerFactory()
        PlayerFriendFactory(player = fede, friend = nico, status = True)

        self.assertEqual(len(fede.games.all()), 0)
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id, 'initial_points': -10 }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nico_invites_fede_when_fede_is_already_playing_A(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Fede plays the game
        fede = PlayerFactory()
        PlayerFriendFactory(player = fede, friend = nico, status = True)
        GamePlayerFactory(player = fede, game = game, status = True)
        
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(fede.games.all()), 1)

    def test_nico_invites_fede_when_fede_is_thinking_is_he_plays(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Fede is thinking is he plays the game
        fede = PlayerFactory()
        PlayerFriendFactory(player = fede, friend = nico, status = True)
        GamePlayerFactory(player = fede, game = game, status = None)
        
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(fede.games.all()), 1)

    def test_nico_invites_fede_when_fede_rejected_to_play(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Fede rejects to play the game
        fede = PlayerFactory()
        PlayerFriendFactory(player = fede, friend = nico, status = True)
        GamePlayerFactory(player = fede, game = game, status = False)
        
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(fede.games.all()), 1)

    def test_nico_invites_fede_after_game_creation_when_they_are_not_friends_A(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico invites Fede to play
        fede = PlayerFactory()
        self.assertEqual(len(fede.games.all()), 0)
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(fede.games.all()), 0)

    def test_nico_invites_fede_after_game_creation_when_they_are_not_friends_B(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico invites Fede to play
        fede = PlayerFactory()
        PlayerFriendFactory(player = fede, friend = nico, status = None)

        self.assertEqual(len(fede.games.all()), 0)
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(fede.games.all()), 0)

    def test_nico_invites_fede_after_game_creation_when_they_are_not_friends_C(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico invites Fede to play
        fede = PlayerFactory()
        PlayerFriendFactory(player = fede, friend = nico, status = False)

        self.assertEqual(len(fede.games.all()), 0)
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(fede.games.all()), 0)

    def test_fede_tries_to_invite_himself_to_nico_game(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede authenticates
        fede = PlayerFactory()
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Fede invites himself to Nico's game
        self.assertEqual(len(fede.games.all()), 0)

        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(fede.games.all()), 0)

    def test_tucu_tries_to_invite_fede_to_nico_game(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Tucu authenticates
        tucu = PlayerFactory()
        token = Token.objects.get(user__username = tucu.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Tucu invites Fede to Nico's game
        fede = PlayerFactory()
        self.assertEqual(len(fede.games.all()), 0)
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(fede.games.all()), 0)

    def test_nico_tries_to_invite_tucu_and_fede(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico and Fede are friends
        fede = PlayerFactory()
        PlayerFriendFactory(player = nico, friend = fede, status = True)

        # Tucu and Fede are friends
        tucu = PlayerFactory()
        PlayerFriendFactory(player = tucu, friend = nico, status = True)

        # Nico invites Fede and Tucu to play
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id }, { 'player':tucu.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(fede.games.all()), 1)
        self.assertEqual(len(tucu.games.all()), 1)

    def test_nico_tries_to_invite_tucu_and_fede_with_initial_points_201_CREATED(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico and Fede are friends
        fede = PlayerFactory()
        PlayerFriendFactory(player = nico, friend = fede, status = True)

        # Tucu and Fede are friends
        tucu = PlayerFactory()
        PlayerFriendFactory(player = tucu, friend = nico, status = True)

        # Nico invites Fede and Tucu to play
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id, 'initial_points': 20 }, { 'player':tucu.id, 'game': game.id, 'initial_points': 10 }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(fede.games.all()), 1)
        self.assertEqual(len(tucu.games.all()), 1)
        self.assertEqual(fede.gameplayer_set.first().initial_points, 20)
        self.assertEqual(tucu.gameplayer_set.first().initial_points, 10)

    def test_nico_tries_to_invite_tucu_fede_when_they_are_not_friends(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico invites Fede and Tucu to play
        fede = PlayerFactory()
        tucu = PlayerFactory()
        url = reverse('gamePlayerCreate')
        data = [{ 'player':fede.id, 'game': game.id }, { 'player':tucu.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(fede.games.all()), 0)
        self.assertEqual(len(tucu.games.all()), 0)


    def test_fede_tries_to_invite_tucu_and_pela_to_nico_game(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede authenticates
        fede = PlayerFactory()
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Fede invites Pela and Tucu to play 
        tucu = PlayerFactory()
        pela = PlayerFactory()
        url = reverse('gamePlayerCreate')
        data = [{ 'player':pela.id, 'game': game.id }, { 'player':tucu.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(tucu.games.all()), 0)
        self.assertEqual(len(pela.games.all()), 0)

    def test_fede_tries_to_invite_tucu_and_pela_to_nico_game_and_nico_to_fede_game(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)

        # Fede authenticates
        fede = PlayerFactory()
        game_fede = GameFactory(owner = fede)
        token = Token.objects.get(user__username = fede.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Fede invites Pela and Tucu to play  Nico's game
        # Fede Nico to play Fede's game
        tucu = PlayerFactory()
        pela = PlayerFactory()
        self.assertEqual(len(tucu.games.all()), 0)
        self.assertEqual(len(pela.games.all()), 0)

        url = reverse('gamePlayerCreate')
        data = [{ 'player': nico.id, 'game': game_fede.id}, {'player':pela.id, 'game': game.id }, { 'player':tucu.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(tucu.games.all()), 0)
        # Nico doesn't have a game because the view is in charge to make the connection with the gamePlayer when the game is created
        self.assertEqual(len(nico.games.all()), 0)
        self.assertEqual(len(pela.games.all()), 0)


    def test_anonymous_tries_to_invites_to_nico_game(self):
        # Nico creates a game
        nico = PlayerFactory()
        game = GameFactory(owner = nico)
        anon = PlayerFactory()

        url = reverse('gamePlayerCreate')
        data = [{ 'player':anon.id, 'game': game.id }]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class GameAPIInitialPointsTest(APITestCase):
    """ 
        CREATE A GAME WITH INITIAL POINTS 
    """

    def test_nico_creates_a_game_with_initial_points_201_CREATED(self):
        tournament = TournamentFactory()
        # Players
        nico = PlayerFactory()
        fede = PlayerFactory()
        tucu = PlayerFactory()

        # Nico is Roberto Carlos
        PlayerFriendFactory(player = nico, friend = fede, status = True)
        PlayerFriendFactory(player = nico, friend = tucu, status = True)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico creates a game
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 
                 'gameplayers' : [{'player':fede.id, 'username': fede.username, 'initial_points': 10}, 
                                  {'player':nico.id, 'username': nico.username, 'initial_points': 0}, 
                                  {'player':tucu.id, 'username': tucu.username, 'initial_points': 5} ]}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(nico.gameplayer_set.first().initial_points, 0)
        self.assertEqual(tucu.gameplayer_set.first().initial_points, 5)
        self.assertEqual(fede.gameplayer_set.first().initial_points, 10)

    def test_nico_creates_a_game_without_initial_points_201_CREATED(self):
        tournament = TournamentFactory()
        # Players
        nico = PlayerFactory()
        fede = PlayerFactory()
        tucu = PlayerFactory()

        # Nico is Roberto Carlos
        PlayerFriendFactory(player = nico, friend = fede, status = True)
        PlayerFriendFactory(player = nico, friend = tucu, status = True)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico creates a game
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 
                 'gameplayers' : [{'player':fede.id, 'username': fede.username }, 
                                  {'player':nico.id, 'username': nico.username }, 
                                  {'player':tucu.id, 'username': tucu.username } ]}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(nico.gameplayer_set.first().initial_points, 0)
        self.assertEqual(tucu.gameplayer_set.first().initial_points, 0)
        self.assertEqual(fede.gameplayer_set.first().initial_points, 0)

    def test_nico_creates_a_game_with_invalid_initial_points_400_BAD_REQUEST(self):
        tournament = TournamentFactory()
        # Players
        nico = PlayerFactory()
        fede = PlayerFactory()
        tucu = PlayerFactory()

        # Nico is Roberto Carlos
        PlayerFriendFactory(player = nico, friend = fede, status = True)
        PlayerFriendFactory(player = nico, friend = tucu, status = True)

        # Nico authenticates
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Nico creates a game
        url = reverse('gameCreate')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 
                 'gameplayers' : [{'player':fede.id, 'username': fede.username, 'initial_points': -10}, 
                                  {'player':nico.id, 'username': nico.username, 'initial_points': 0}, 
                                  {'player':tucu.id, 'username': tucu.username, 'initial_points': 5} ]}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GameAPIFixturePointsTest(APITestCase):
    """ 
        GAME WITH FIXTURE POINTS 

        We get the game with a list of the fixture points of the players
    """
    def test_get_game_with_fixture_points_200_OK(self):
        # Game Player
        gp = GamePlayerFactory(status = True) # The game is an Exact Game

        # Fixture Player Points
        FixturePlayerPointsFactory(gameplayer = gp)

        # Player authenticates
        token = Token.objects.get(user__username = gp.player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameList')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data[0]['gameplayers'][0].has_key('fixture_points'))
        self.assertTrue(response.data[0]['gameplayers'][0]['fixture_points'][0].has_key('classic_prediction'))

    def test_get_game_with_multiple_fixture_points_200_OK(self):
        # Game Player
        gp = GamePlayerFactory(status = True) # The game is an Exact Game

        # Fixture Player Points
        FixturePlayerPointsFactory(gameplayer = gp)
        FixturePlayerPointsFactory(gameplayer = gp)

        # Player authenticates
        token = Token.objects.get(user__username = gp.player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameList')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data[0]['gameplayers'][0].has_key('fixture_points'))
        self.assertEqual(len(response.data[0]['gameplayers'][0]['fixture_points']), 2)
        self.assertTrue(response.data[0]['gameplayers'][0]['fixture_points'][0].has_key('classic_prediction'))
        self.assertTrue(response.data[0]['gameplayers'][0]['fixture_points'][1].has_key('classic_prediction'))

    def test_get_game_with_multiple_fixture_points_and_multiples_players_200_OK(self):
        # Game Player
        gp_1 = GamePlayerFactory(status = True) # The game is an Exact Game
        gp_2 = GamePlayerFactory(status = True, game = gp_1.game)

        # Fixture Player 1 Points
        FixturePlayerPointsFactory(gameplayer = gp_1)
        FixturePlayerPointsFactory(gameplayer = gp_1)

        # Fixture Player 2 Points
        FixturePlayerPointsFactory(gameplayer = gp_2)

        # Player authenticates
        token = Token.objects.get(user__username = gp_1.player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameList')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]['gameplayers'][0]['fixture_points']), 2)
        self.assertEqual(len(response.data[0]['gameplayers'][1]['fixture_points']), 1)

