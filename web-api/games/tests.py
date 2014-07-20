import unittest
from datetime import datetime, timedelta
from django.test import TestCase
from tournaments.models import Team, Fixture, Match
from .models import Player
from .factories import *

class TournamentTest(TestCase):
    def test_the_player_setting_fixtures_results(self):
        # Matchs
        tournament = TournamentFactory()
        match = MatchFactory()

        # Player
        player = PlayerFactory()
        player.make_prediction(match.pk, 0, 0)

        self.assertEqual(len(player.playermatchprediction_set.all()), 1)
        self.assertEqual(1, 1)

class ExactPredictionTest(TestCase):
    def test_prediction_ok(self):
        match_1 = MatchFactory()

        player_prediction = \
                PlayerMatchPredictionFactory(visitor_team_goals = match_1.visitor_team_goals, 
                                            local_team_goals = match_1.local_team_goals, 
                                            match = match_1)

        self.assertTrue(player_prediction.is_a_exact_prediction())

    def test_prediction_not_ok(self):
        match_2 = MatchFactory()
        player_prediction = \
                PlayerMatchPredictionFactory(visitor_team_goals = (match_2.visitor_team_goals + 1), 
                                            local_team_goals = match_2.local_team_goals, 
                                            match = match_2)

        self.assertFalse(player_prediction.is_a_exact_prediction())

class MoralPredictionTest(TestCase):
    def test_same_goals_prediction_true(self):
        match = MatchFactory()

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = match.visitor_team_goals, 
                                       local_team_goals = match.local_team_goals, 
                                       match = match)


        self.assertTrue(player_prediction.is_a_moral_prediction())

    def test_visitor_team_wins_prediction_true(self):
        match = MatchFactory(visitor_team_goals = 2, 
                             local_team_goals = 0)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = 3, 
                                       local_team_goals = 0, 
                                       match = match)

        self.assertTrue(player_prediction.is_a_moral_prediction())

    def test_draw_prediction_true(self):
        match = MatchFactory(visitor_team_goals = 0, 
                             local_team_goals = 0)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = 0, 
                                       local_team_goals = 0, 
                                       match = match)

        self.assertTrue(player_prediction.is_a_moral_prediction())

    def test_draw_prediction_with_differents_goals_true(self):
        match = MatchFactory(visitor_team_goals = 0, 
                             local_team_goals = 0)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = 1, 
                                       local_team_goals = 1, 
                                       match = match)
 
        self.assertTrue(player_prediction.is_a_moral_prediction())

    def test_local_team_wins_prediction_false(self):
        match = MatchFactory(visitor_team_goals = 0, 
                             local_team_goals = 0)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = 0, 
                                       local_team_goals = 1, 
                                       match = match)

        self.assertFalse(player_prediction.is_a_moral_prediction())

    def test_draw_prediction_false(self):
        match = MatchFactory(visitor_team_goals = 1, 
                             local_team_goals = 0)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = 0, 
                                       local_team_goals = 0, 
                                       match = match)

        self.assertFalse(player_prediction.is_a_moral_prediction())

    def test_visitor_team_wins_prediction_false(self):
        match = MatchFactory(visitor_team_goals = 1, 
                             local_team_goals = 2)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = 2, 
                                       local_team_goals = 1, 
                                       match = match)

        self.assertFalse(player_prediction.is_a_moral_prediction())

class DPGamePlayerPointsTest(TestCase):
    def test_player_points_from_one_correct_exact_prediction(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(3, fixture_points)

    def test_player_points_from_some_exact_prediction_and_some_not(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        fixture = FixtureFactory(is_finished = True)
        # Match 1
        match = MatchFactory(fixture = fixture, visitor_team_goals = 2, local_team_goals = 0)
        match_prediction_true = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        match_prediction_false = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 2)

        # Match 2
        match_2 = MatchFactory(fixture = fixture, visitor_team_goals = 0, local_team_goals = 2)
        match_prediction_2_false = \
                PlayerMatchPredictionFactory(match = match_2,
                                           player = player, 
                                           visitor_team_goals = 2,
                                           local_team_goals = 0)


        self.assertTrue(match_prediction_true.is_a_exact_prediction())
        self.assertFalse(match_prediction_false.is_a_exact_prediction())
        self.assertFalse(match_prediction_2_false.is_a_exact_prediction())

        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(3, fixture_points)

    def test_player_points_from_one_moral_prediction(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals + 1,
                                           local_team_goals = match.local_team_goals + 1)

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(1, fixture_points)

    def test_player_points_from_some_moral_prediction_and_some_not(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        fixture = FixtureFactory(is_finished = True)
        # Match 1
        match = MatchFactory(fixture = fixture, visitor_team_goals = 2, local_team_goals = 0)
        match_prediction_true = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = 3,
                                           local_team_goals = 0)

        match_prediction_false = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 2)

        # Match 2
        match_2 = MatchFactory(fixture = fixture, visitor_team_goals = 0, local_team_goals = 2)
        match_prediction_2_false = \
                PlayerMatchPredictionFactory(match = match_2,
                                           player = player, 
                                           visitor_team_goals = 1,
                                           local_team_goals = 0)

        match_prediction_2_true = \
                PlayerMatchPredictionFactory(match = match_2,
                                           player = player, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 4)

        self.assertTrue(match_prediction_true.is_a_moral_prediction())
        self.assertFalse(match_prediction_false.is_a_moral_prediction())

        self.assertFalse(match_prediction_2_false.is_a_moral_prediction())
        self.assertTrue(match_prediction_2_true.is_a_moral_prediction())

        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(2, fixture_points)

    def test_player_points_from_moral_and_exact_predictions(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        fixture = FixtureFactory(is_finished = True)

        # Match 1
        match = MatchFactory(fixture = fixture, visitor_team_goals = 2, local_team_goals = 0)
        match_exact_prediction_true = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = 2,
                                           local_team_goals = 0) # points = 3

        match_exact_prediction_false = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 2) # points = 0

        match_exact_prediction_false_moral_prediction_true = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = 4,
                                           local_team_goals = 3) # points = 1

        # Match 2
        match_2 = MatchFactory(fixture = fixture, visitor_team_goals = 0, local_team_goals = 2)
        match_2_exact_prediction_false_moral_prediction_true = \
                PlayerMatchPredictionFactory(match = match_2,
                                           player = player, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 4) # points = 1

        # Match 3
        match_3 = MatchFactory(fixture = fixture )
        match_3_exact_prediction_true = \
                PlayerMatchPredictionFactory(match = match_3,
                                           player = player, 
                                           visitor_team_goals = match_3.visitor_team_goals,
                                           local_team_goals = match_3.local_team_goals) # points = 3

        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(8, fixture_points)

    def test_player_points_from_one_correct_exact_prediction_of_a_classic_match(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(6, fixture_points)

    def test_player_points_from_one_correct_moral_prediction_of_a_classic_match(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(2, fixture_points)

    def test_player_points_from_one_correct_exact_prediction_with_double(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           is_double = True,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(6, fixture_points)

    def test_player_points_from_one_correct_moral_prediction_with_double(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           is_double = True,
                                           player = player, 
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(2, fixture_points)

    def test_get_player_points_from_one_correct_exact_prediction_with_double_of_a_classic_match(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           is_double = True,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(12, fixture_points)

    def test_player_points_from_one_correct_moral_prediction_with_double_of_a_classic_match(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           is_double = True,
                                           player = player, 
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(4, fixture_points)

    def test_player_points_with_initial_points(self):
        player = PlayerFactory(initial_points = 2)
        game = GameFactory(owner = player)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(5, fixture_points)

class ClassicGamePlayerPointsTest(TestCase):
    def test_draw_prediction_false(self):
        fixture = FixtureFactory(is_finished = True)
        player = PlayerFactory()
        game = GameFactory(classic = True, owner = player)
        match = MatchFactory(fixture = fixture,
                             is_classic = True, 
                             visitor_team_goals = 0,
                             local_team_goals = 1) 
        player_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 0)

        self.assertFalse(player_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(0, fixture_points)

    def test_draw_prediction_true(self):
        fixture = FixtureFactory(is_finished = True)
        player = PlayerFactory()
        game = GameFactory(classic = True, owner = player)
        match = MatchFactory(fixture = fixture,
                             is_classic = True, 
                             visitor_team_goals = 0,
                             local_team_goals = 0) 
        player_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 0)

        self.assertTrue(player_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(1, fixture_points)

    def test_win_prediction_true(self):
        fixture = FixtureFactory(is_finished = True)
        player = PlayerFactory()
        game = GameFactory(classic = True, owner = player)
        match = MatchFactory(fixture = fixture,
                             is_classic = True, 
                             visitor_team_goals = 2,
                             local_team_goals = 0) 
        player_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = 3,
                                           local_team_goals = 0)

        self.assertTrue(player_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(1, fixture_points)

    def test_multiples_predictions(self):
        fixture = FixtureFactory(is_finished = True)
        player = PlayerFactory()
        game = GameFactory(classic = True, owner = player)
        # Prediction ok
        match = MatchFactory(fixture = fixture,
                             is_classic = True, 
                             visitor_team_goals = 2,
                             local_team_goals = 0) 
        player_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = 3,
                                           local_team_goals = 0)

        # Prediction not ok
        match_1 = MatchFactory(is_classic = True, 
                             visitor_team_goals = 2,
                             local_team_goals = 0) 
        player_prediction_1 = \
                PlayerMatchPredictionFactory(match = match_1,
                                           player = player, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 0)

        # Prediction ok
        match_2 = MatchFactory(fixture = fixture,
                             is_classic = True, 
                             visitor_team_goals = 0,
                             local_team_goals = 0) 
        player_prediction_2 = \
                PlayerMatchPredictionFactory(match = match_2,
                                           player = player, 
                                           visitor_team_goals = 2,
                                           local_team_goals = 2)

        self.assertTrue(player_prediction.is_a_moral_prediction())
        self.assertFalse(player_prediction_1.is_a_moral_prediction())
        self.assertTrue(player_prediction_2.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(2, fixture_points)

    def test_fixture_points(self):
        game = GameFactory(classic = True)
        player = PlayerFactory()
        game = GameFactory(classic = True, owner = player)
        fixture = FixtureFactory(is_finished = True)
        fixture_2 = FixtureFactory(tournament = fixture.tournament, is_finished = True)
        # Prediction ok
        match = MatchFactory(is_classic = True, 
                             fixture = fixture,
                             visitor_team_goals = 2,
                             local_team_goals = 0) 
        player_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = 3,
                                           local_team_goals = 0)

        # Prediction ok
        match_1 = MatchFactory(is_classic = True, 
                             fixture = fixture,
                             visitor_team_goals = 2,
                             local_team_goals = 0) 
        player_prediction_1 = \
                PlayerMatchPredictionFactory(match = match_1,
                                           player = player, 
                                           visitor_team_goals = 2,
                                           local_team_goals = 0)

        # Prediction ok
        match_2 = MatchFactory(fixture = fixture_2,
                             is_classic = True, 
                             visitor_team_goals = 0,
                             local_team_goals = 0) 
        player_prediction_2 = \
                PlayerMatchPredictionFactory(match = match_2,
                                           player = player, 
                                           visitor_team_goals = 2,
                                           local_team_goals = 2)

        # Match suspended
        match_3 = MatchFactory(fixture = fixture_2,
                             is_classic = True, 
                             suspended = True,
                             visitor_team_goals = 0,
                             local_team_goals = 0) 

        player_prediction_3 = \
                PlayerMatchPredictionFactory(match = match_3,
                                           player = player, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 0)

        fixture_points = player.get_fixture_points(fixture, game)
        self.assertEqual(2, fixture_points)

        fixture2_points = player.get_fixture_points(fixture_2, game)
        self.assertEqual(1, fixture2_points)

        fixture_points = FixturePlayerPointsFactory(fixture = fixture, 
                                                    game = game,
                                                    player = player,
                                                    points = fixture_points)

        fixture_points = FixturePlayerPointsFactory(fixture = fixture_2, 
                                                    game = game,
                                                    player = player,
                                                    points = fixture2_points)
        self.assertEqual(3, player.get_total_points(game))


class TournamentFixtureTest(TestCase):
    def test_get_current_fixture(self):
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, is_finished = True)
        fixture_3 = FixtureFactory(tournament = tournament, is_finished = False)
        fixture_4 = FixtureFactory(tournament = tournament, is_finished = False)

        self.assertEqual(fixture_3.number, tournament.get_current_fixture().number)

    def test_tournament_without_fixtures(self):
        tournament = TournamentFactory()
        self.assertFalse(tournament.get_current_fixture())

    def test_if_there_is_not_current_fixtures_get_the_last_one(self):
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, is_finished = True)
        self.assertTrue(tournament.get_current_fixture())

class FixturePredictionsTest(TestCase):
    def test_get_fixture_predictions(self):
        player = PlayerFactory()
        fixture_1 = FixtureFactory()
        match_1 = MatchFactory(fixture = fixture_1)
        match_2 = MatchFactory(fixture = fixture_1)

        fixture_2 = FixtureFactory()
        match_3 = MatchFactory(fixture = fixture_2)

        PlayerMatchPredictionFactory(match = match_1, 
                                     player = player)
        PlayerMatchPredictionFactory(match = match_2, 
                                     player = player)

        self.assertEqual(2, len(player.get_fixture_predictions(fixture_1)))
        self.assertFalse(player.get_fixture_predictions(fixture_2))

# REST API
import json
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .serializers import GameSerializer

class GameAPITest(APITestCase):
    def test_get_200_OK(self):
        player = PlayerFactory()
        game_1 = GameFactory(owner = player)
        game_2 = GameFactory(owner = player)

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameList')
        response = self.client.get(url)
        r_games = json.loads(response.content)

        self.assertEqual(r_games[0]['name'], game_1.name)
        self.assertEqual(r_games[1]['name'], game_2.name)
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

        url = reverse('gameList')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers': [] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_401_UNAUTHORIZED(self):
        player = PlayerFactory()
        tournament = TournamentFactory()

        url = reverse('gameList')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_get_200_OK(self):
        player = PlayerFactory()
        tournament = TournamentFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Create two games
        url = reverse('gameList')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers': [] }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = { 'name' : 'Game 2', 'tournament': tournament.pk, 'gameplayers': [] }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get Games
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
        url = reverse('gameList')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers': [] }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get
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

    def test_create_with_two_players_200_OK(self):
        # The owner is a player
        owner = PlayerFactory()
        token = Token.objects.get(user__username = owner.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        player = PlayerFactory()
        tournament = TournamentFactory()

        # Create 
        url = reverse('gameList')
        data = { 'name' : 'Game 1', 'tournament': tournament.pk, 'gameplayers' : [{'player':player.id}] }
        response = self.client.post(url, data, format='json')

        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.all()[0].players.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class PlayerAPITest(APITestCase):
    def test_create_200_OK(self): 
        data = { 'username': 'nico',
                 'email': 'nmbases@gmail.com',
                 'password': 'nico' }

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
                 'password': 'nico' }

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

