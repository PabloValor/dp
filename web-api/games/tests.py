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

        # Player is playing a game
        gp = GamePlayerFactory(status = True)
        player = gp.player

        # Player makes a predictions
        player.make_prediction(gp.id, match.pk, 0, 0)

        self.assertEqual(PlayerMatchPrediction.objects.count(), 1)

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
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)

        fixture = FixtureFactory(is_finished = True)

        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(3, fixture_points)

    def test_player_points_from_some_exact_prediction_and_some_not(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        # Match 1
        match = MatchFactory(fixture = fixture, visitor_team_goals = 2, local_team_goals = 0)
        match_prediction_true = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        match_prediction_false = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 2)

        # Match 2
        match_2 = MatchFactory(fixture = fixture, visitor_team_goals = 0, local_team_goals = 2)
        match_prediction_2_false = \
                PlayerMatchPredictionFactory(match = match_2,
                                           gameplayer = gameplayer,
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
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals + 1,
                                           local_team_goals = match.local_team_goals + 1)

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(1, fixture_points)

    def test_player_points_from_some_moral_prediction_and_some_not(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        # Match 1
        match = MatchFactory(fixture = fixture, visitor_team_goals = 2, local_team_goals = 0)
        match_prediction_true = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 3,
                                           local_team_goals = 0)

        match_prediction_false = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 2)

        # Match 2
        match_2 = MatchFactory(fixture = fixture, visitor_team_goals = 0, local_team_goals = 2)
        match_prediction_2_false = \
                PlayerMatchPredictionFactory(match = match_2,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 1,
                                           local_team_goals = 0)

        match_prediction_2_true = \
                PlayerMatchPredictionFactory(match = match_2,
                                           gameplayer = gameplayer,
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
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)

        # Match 1
        match = MatchFactory(fixture = fixture, visitor_team_goals = 2, local_team_goals = 0)
        match_exact_prediction_true = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 2,
                                           local_team_goals = 0) # points = 3

        match_exact_prediction_false = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 2) # points = 0

        match_exact_prediction_false_moral_prediction_true = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 4,
                                           local_team_goals = 3) # points = 1

        # Match 2
        match_2 = MatchFactory(fixture = fixture, visitor_team_goals = 0, local_team_goals = 2)
        match_2_exact_prediction_false_moral_prediction_true = \
                PlayerMatchPredictionFactory(match = match_2,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 4) # points = 1

        # Match 3
        match_3 = MatchFactory(fixture = fixture )
        match_3_exact_prediction_true = \
                PlayerMatchPredictionFactory(match = match_3,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match_3.visitor_team_goals,
                                           local_team_goals = match_3.local_team_goals) # points = 3

        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(8, fixture_points)

    def test_player_points_from_one_correct_exact_prediction_of_a_classic_match(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(6, fixture_points)

    def test_player_points_from_one_correct_moral_prediction_of_a_classic_match(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(2, fixture_points)

    def test_player_points_from_one_correct_exact_prediction_with_double(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           is_double = True,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(6, fixture_points)

    def test_player_points_from_one_correct_moral_prediction_with_double(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           is_double = True,
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(2, fixture_points)

    def test_get_player_points_from_one_correct_exact_prediction_with_double_of_a_classic_match(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           is_double = True,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(12, fixture_points)

    def test_player_points_from_one_correct_moral_prediction_with_double_of_a_classic_match(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           is_double = True,
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(4, fixture_points)

    def test_player_points_with_initial_points(self):
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True, initial_points = 2)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
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

        gameplayer = GamePlayerFactory(player = player, game = game, status = True)

        match = MatchFactory(fixture = fixture,
                             is_classic = True, 
                             visitor_team_goals = 0,
                             local_team_goals = 1) 
        player_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 0)

        self.assertFalse(player_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(0, fixture_points)

    def test_draw_prediction_true(self):
        fixture = FixtureFactory(is_finished = True)
        player = PlayerFactory()
        game = GameFactory(classic = True, owner = player)
        gameplayer = GamePlayerFactory(player = player, game = game, status = True)
        match = MatchFactory(fixture = fixture,
                             is_classic = True, 
                             visitor_team_goals = 0,
                             local_team_goals = 0) 
        player_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 0)

        self.assertTrue(player_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(1, fixture_points)

    def test_win_prediction_true(self):
        fixture = FixtureFactory(is_finished = True)
        player = PlayerFactory()
        game = GameFactory(classic = True, owner = player)
        gameplayer = GamePlayerFactory(player = player, game = game, status = True)
        match = MatchFactory(fixture = fixture,
                             is_classic = True, 
                             visitor_team_goals = 2,
                             local_team_goals = 0) 
        player_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 3,
                                           local_team_goals = 0)

        self.assertTrue(player_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture, game)
        self.assertEqual(1, fixture_points)

    def test_multiples_predictions(self):
        fixture = FixtureFactory(is_finished = True)
        player = PlayerFactory()
        game = GameFactory(classic = True, owner = player)
        gameplayer = GamePlayerFactory(player = player, game = game, status = True)
        # Prediction ok
        match = MatchFactory(fixture = fixture,
                             is_classic = True, 
                             visitor_team_goals = 2,
                             local_team_goals = 0) 
        player_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 3,
                                           local_team_goals = 0)

        # Prediction not ok
        match_1 = MatchFactory(is_classic = True, 
                             visitor_team_goals = 2,
                             local_team_goals = 0) 
        player_prediction_1 = \
                PlayerMatchPredictionFactory(match = match_1,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 0)

        # Prediction ok
        match_2 = MatchFactory(fixture = fixture,
                             is_classic = True, 
                             visitor_team_goals = 0,
                             local_team_goals = 0) 
        player_prediction_2 = \
                PlayerMatchPredictionFactory(match = match_2,
                                           gameplayer = gameplayer,
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
        gameplayer = GamePlayerFactory(player = player, game = game, status = True)
        fixture = FixtureFactory(is_finished = True)
        fixture_2 = FixtureFactory(tournament = fixture.tournament, is_finished = True)
        # Prediction ok
        match = MatchFactory(is_classic = True, 
                             fixture = fixture,
                             visitor_team_goals = 2,
                             local_team_goals = 0) 
        player_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 3,
                                           local_team_goals = 0)

        # Prediction ok
        match_1 = MatchFactory(is_classic = True, 
                             fixture = fixture,
                             visitor_team_goals = 2,
                             local_team_goals = 0) 
        player_prediction_1 = \
                PlayerMatchPredictionFactory(match = match_1,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 2,
                                           local_team_goals = 0)

        # Prediction ok
        match_2 = MatchFactory(fixture = fixture_2,
                             is_classic = True, 
                             visitor_team_goals = 0,
                             local_team_goals = 0) 
        player_prediction_2 = \
                PlayerMatchPredictionFactory(match = match_2,
                                           gameplayer = gameplayer,
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
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 0)

        fixture_points = player.get_fixture_points(fixture, game)
        self.assertEqual(2, fixture_points)

        fixture2_points = player.get_fixture_points(fixture_2, game)
        self.assertEqual(1, fixture2_points)

        fixture_points = FixturePlayerPointsFactory(fixture = fixture, 
                                                    gameplayer = gameplayer,
                                                    points = fixture_points)

        fixture_points = FixturePlayerPointsFactory(fixture = fixture_2, 
                                                    gameplayer = gameplayer,
                                                    points = fixture2_points)

        self.assertEqual(3, player.get_total_points(game))


class FixturePredictionsTest(TestCase):
    def test_get_fixture_predictions(self):
        gp = GamePlayerFactory(status = True)
        player = gp.player

        fixture_1 = FixtureFactory()
        match_1 = MatchFactory(fixture = fixture_1)
        match_2 = MatchFactory(fixture = fixture_1)

        fixture_2 = FixtureFactory()
        match_3 = MatchFactory(fixture = fixture_2)

        PlayerMatchPredictionFactory(match = match_1, 
                                     gameplayer = gp)
        PlayerMatchPredictionFactory(match = match_2, 
                                     gameplayer = gp)

        self.assertEqual(2, len(player.get_fixture_predictions(fixture_1, gp.game)))
        self.assertFalse(player.get_fixture_predictions(fixture_2, gp.game))

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
        game_1 = GamePlayerFactory(player = player)
        game_2 = GamePlayerFactory(player = player)

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('gameList')
        response = self.client.get(url)
        r_games = json.loads(response.content)

        self.assertEqual(r_games[0]['name'], game_1.game.name)
        self.assertEqual(r_games[1]['name'], game_2.game.name)
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
        PLAYER REQUEST FOR ANOTHER INVITATION AFTER HE REJECTED THE FIRST ONE

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

    def test_nico_does_a_prediction_of_a_finished_match_400_BAD_REQUEST(self):
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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_nico_does_a_prediction_of_a_finished_fixture_400_BAD_REQUEST(self):
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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_nico_does_a_prediction_of_an_unexisting_match_400_BAD_REQUEST(self):
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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
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

    def test_fede_tries_to_do_a_prediction_as_nico_HTTP_400_BAD_REQUEST(self):
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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_nico_does_two_predictions_for_the_same_match_the_first_one_is_deleed_201_CREATED(self):
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

    def test_nico_does_a_prediction_of_a_game_that_he_isnt_playing_400_BAD_REQUEST_A(self):
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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_nico_does_a_prediction_of_a_game_that_he_isnt_playing_400_BAD_REQUEST_B(self):
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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(gp.match_predictions.count(), 0)

    def test_nico_does_a_prediction_of_a_fixture_already_closed_400_BAD_REQUEST(self):
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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
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
