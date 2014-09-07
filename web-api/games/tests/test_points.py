import unittest
from datetime import datetime, timedelta
from django.test import TestCase
from tournaments.models import Team, Fixture, Match
from ..models import Player, FixturePlayerPoints
from ..factories import *

class ExactPredictionTest(TestCase):
    def test_prediction_ok(self):
        match_1 = MatchFactory(is_finished = True)

        player_prediction = \
                PlayerMatchPredictionFactory(visitor_team_goals = match_1.visitor_team_goals, 
                                            local_team_goals = match_1.local_team_goals, 
                                            match = match_1)

        self.assertTrue(player_prediction.is_exact_prediction())

    def test_prediction_not_ok(self):
        match_2 = MatchFactory()
        player_prediction = \
                PlayerMatchPredictionFactory(visitor_team_goals = (match_2.visitor_team_goals + 1), 
                                            local_team_goals = match_2.local_team_goals, 
                                            match = match_2)

        self.assertFalse(player_prediction.is_exact_prediction())

class GeneralPredictionTest(TestCase):
    def test_same_goals_prediction_true(self):
        match = MatchFactory(is_finished = True)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = match.visitor_team_goals, 
                                       local_team_goals = match.local_team_goals, 
                                       match = match)


        self.assertTrue(player_prediction.is_general_prediction())

    def test_visitor_team_wins_prediction_true(self):
        match = MatchFactory(visitor_team_goals = 2, is_finished = True,
                             local_team_goals = 0)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = 3, 
                                       local_team_goals = 0, 
                                       match = match)

        self.assertTrue(player_prediction.is_general_prediction())

    def test_draw_prediction_true(self):
        match = MatchFactory(visitor_team_goals = 0, 
                             is_finished = True,
                             local_team_goals = 0)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = 0, 
                                       local_team_goals = 0, 
                                       match = match)

        self.assertTrue(player_prediction.is_general_prediction())

    def test_draw_prediction_with_differents_goals_true(self):
        match = MatchFactory(visitor_team_goals = 0, 
                             is_finished = True,
                             local_team_goals = 0)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = 1, 
                                       local_team_goals = 1, 
                                       match = match)
 
        self.assertTrue(player_prediction.is_general_prediction())

    def test_local_team_wins_prediction_false(self):
        match = MatchFactory(visitor_team_goals = 0, 
                             local_team_goals = 0)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = 0, 
                                       local_team_goals = 1, 
                                       match = match)

        self.assertFalse(player_prediction.is_general_prediction())

    def test_draw_prediction_false(self):
        match = MatchFactory(visitor_team_goals = 1, 
                             local_team_goals = 0)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = 0, 
                                       local_team_goals = 0, 
                                       match = match)

        self.assertFalse(player_prediction.is_general_prediction())

    def test_visitor_team_wins_prediction_false(self):
        match = MatchFactory(visitor_team_goals = 1, 
                             local_team_goals = 2)

        player_prediction = \
            PlayerMatchPredictionFactory(visitor_team_goals = 2, 
                                       local_team_goals = 1, 
                                       match = match)

        self.assertFalse(player_prediction.is_general_prediction())

class ExactGamePlayerPointsTest(TestCase):
    def test_player_exact_prediction_points_A(self):
        """ 
          Matches: 1
          Predictions: 1
          Predictions with points: 1
          Points: 6 (3 x Exact Score, 3 x General Score)

          Wins local team
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)

        fixture = FixtureFactory(is_finished = True)

        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 1)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_exact_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(6, fixture_points)

    def test_player_exact_prediction_points_B(self):
        """ 
          Matches: 1
          Predictions: 1
          Predictions with points: 1
          Points: 6 (3 x Exact Score, 3 x General Score)

          Wins visitor team
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)

        fixture = FixtureFactory(is_finished = True)

        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 1, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_exact_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(6, fixture_points)

    def test_player_exact_prediction_points_C(self):
        """ 
          Matches: 1
          Predictions: 1
          Predictions with points: 1
          Points: 6 (3 x Exact Score, 3 x General Score)

          Draw 
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)

        fixture = FixtureFactory(is_finished = True)

        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_exact_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(6, fixture_points)


    def test_player_general_prediction_points_A(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 3 (3 x General Score)

          Wins local
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 1)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals + 1,
                                           local_team_goals = match.local_team_goals + 1)

        self.assertTrue(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(3, fixture_points)

    def test_player_general_prediction_points_B(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 3 (3 x General Score)

          Wins Visitor
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 1, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals + 1,
                                           local_team_goals = match.local_team_goals + 1)

        self.assertTrue(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(3, fixture_points)

    def test_player_general_prediction_points_C(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 3 (3 x General Score)

          Draw 
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals + 1,
                                           local_team_goals = match.local_team_goals + 1)

        self.assertTrue(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(3, fixture_points)

    def test_player_bad_prediction_points_A(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0 (0 x General Score)

          Bad prediction
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 1, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 1)

        self.assertFalse(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)

    def test_player_bad_prediction_points_B(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0 (0 x General Score)

          Bad prediction
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 1)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 1,
                                           local_team_goals = 0)

        self.assertFalse(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)

    def test_player_bad_prediction_points_C(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0 (0 x General Score)

          Bad prediction
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 1,
                                           local_team_goals = 0)

        self.assertFalse(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)

    def test_player_bad_prediction_points_D(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0 (0 x General Score)

          Bad prediction
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 1)

        self.assertFalse(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)

    def test_player_match_not_finished_points_A(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0 (0 x General Score)

          Match is not finished: general prediction
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = False, visitor_team_goals = 0, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 1,
                                           local_team_goals = 1)

        self.assertFalse(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)

    def test_player_match_not_finished_points_B(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0 (0 x General Score)

          Match is not finished: exact prediction
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = False, visitor_team_goals = 1, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 1,
                                           local_team_goals = 0)

        self.assertFalse(match_prediction.is_exact_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)

    def test_player_exact_prediction_points_multiples_match_A(self):
        """ 
          Match: 2
          Predictions: 3 
          Predictions with points: 1
          Points: 6 (3 x Exact Score, 3 x General Score)
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        # Match 1
        match = MatchFactory(fixture = fixture, visitor_team_goals = 2, local_team_goals = 0, is_finished = True)
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


        self.assertTrue(match_prediction_true.is_exact_prediction())
        self.assertFalse(match_prediction_false.is_exact_prediction())
        self.assertFalse(match_prediction_2_false.is_exact_prediction())

        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(6, fixture_points)

    def test_player_exact_prediction_points_multiples_match_B(self):
        """ 
          Match: 2
          Predictions: 4 
          Predictions with points: 2
          Points: 6 (6 x General Score)
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        # Match 1
        match = MatchFactory(fixture = fixture, visitor_team_goals = 2, local_team_goals = 0, is_finished = True)
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
        match_2 = MatchFactory(fixture = fixture, visitor_team_goals = 0, local_team_goals = 2, is_finished = True)
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

        self.assertTrue(match_prediction_true.is_general_prediction())
        self.assertFalse(match_prediction_false.is_general_prediction())

        self.assertFalse(match_prediction_2_false.is_general_prediction())
        self.assertTrue(match_prediction_2_true.is_general_prediction())

        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(6, fixture_points)

    def test_player_exact_prediction_points_multiples_match_C(self):
        """ 
          Match: 3
          Predictions: 4 
          Predictions with points: 12
          Points: 6 (9 x General Score, 3 x Exact Prediction)
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)

        # Match 1
        match = MatchFactory(fixture = fixture, visitor_team_goals = 2, local_team_goals = 0, is_finished = True)

        # General and Exact Prediction
        PlayerMatchPredictionFactory(match = match,
                                    gameplayer = gameplayer,
                                    visitor_team_goals = 2,
                                    local_team_goals = 0) # points = 6

        # Awful Prediction
        PlayerMatchPredictionFactory(match = match,
                                    gameplayer = gameplayer,
                                    visitor_team_goals = 0,
                                    local_team_goals = 2) # points = 0

        # General Prediction
        PlayerMatchPredictionFactory(match = match,
                                    gameplayer = gameplayer,
                                    visitor_team_goals = 4,
                                    local_team_goals = 3) # points = 3

        # Match 2
        match_2 = MatchFactory(fixture = fixture, visitor_team_goals = 0, local_team_goals = 2, is_finished = True)

        # General Prediction
        PlayerMatchPredictionFactory(match = match_2,
                                    gameplayer = gameplayer,
                                    visitor_team_goals = 0,
                                    local_team_goals = 4) # points = 3

        # Match 3
        match_3 = MatchFactory(fixture = fixture )

        # General Prediction
        PlayerMatchPredictionFactory(match = match_3,
                                    gameplayer = gameplayer,
                                    visitor_team_goals = match_3.visitor_team_goals,
                                    local_team_goals = match_3.local_team_goals) # points = 3

        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(12, fixture_points)

    def test_player_exact_prediction_points_in_classic_match_A(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1 
          Points: 8 (3 x General Score, 3 x Exact Prediction, 2 x Classic)
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)

        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True, is_finished = True)

        match_prediction = PlayerMatchPredictionFactory(match = match,
                                    gameplayer = gameplayer,
                                    visitor_team_goals = match.visitor_team_goals,
                                    local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_exact_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(8, fixture_points)

    def test_player_exact_prediction_points_in_classic_match_B(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1 
          Points: 5 (3 x General Score, 2 x Classic)
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)

        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True, is_finished = True)

        match_prediction = PlayerMatchPredictionFactory(match = match,
                                    gameplayer = gameplayer,
                                    visitor_team_goals = (match.visitor_team_goals + 1),
                                    local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(5, fixture_points)

    def test_player_exact_prediction_points_in_classic_match_C(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)

        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True, is_finished = True,
                            visitor_team_goals = 2, local_team_goals = 0)

        match_prediction = PlayerMatchPredictionFactory(match = match,
                                    gameplayer = gameplayer,
                                    visitor_team_goals = 0,
                                    local_team_goals = 2)

        self.assertFalse(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)

    def test_player_exact_prediction_points_with_double_A(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1 
          Points: 12 (3 x General Score, 3 x Exact Prediction, 6 x Double)
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           is_double = True,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_exact_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(12, fixture_points)

    def test_player_exact_prediction_points_with_double_B(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1 
          Points: 6 (3 x General Score, 3 x Double)
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           is_double = True,
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(6, fixture_points)

    def test_player_exact_prediction_points_with_double_and_classic_A(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1 
          Points: 16 (3 x General Score, 2 x Classic, 3 x Exact Score, 8 x Double)
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True, is_finished = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           is_double = True,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_exact_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(16, fixture_points)

    def test_player_exact_prediction_points_with_double_and_classic_B(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1 
          Points: 10 (3 x General Score, 2 x Classic, 5 x Double)
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True, is_finished = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           is_double = True,
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(10, fixture_points)

    def test_player_points_with_initial_points(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1 
          Points: 8 (3 x General Score, 3 x Exact Prediction, 2 x Initial Points)
        """
        player = PlayerFactory()
        game = GameFactory(owner = player)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True, initial_points = 2)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(8, fixture_points)

class GeneralGamePlayerPointsTest(TestCase):
    def test_player_exact_prediction_points_A(self):
        """ 
          Matches: 1
          Predictions: 1
          Predictions with points: 1
          Points: 3 (3 x General Score)

          Wins local team
        """
        player = PlayerFactory()
        game = GameFactory(owner = player, classic = True)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)

        fixture = FixtureFactory(is_finished = True)

        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 1)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_exact_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(3, fixture_points)

    def test_player_exact_prediction_points_B(self):
        """ 
          Matches: 1
          Predictions: 1
          Predictions with points: 1
          Points: 3 (3 x General Score)

          Wins visitor team
        """
        player = PlayerFactory()
        game = GameFactory(owner = player, classic = True)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)

        fixture = FixtureFactory(is_finished = True)

        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 1, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_exact_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(3, fixture_points)

    def test_player_exact_prediction_points_C(self):
        """ 
          Matches: 1
          Predictions: 1
          Predictions with points: 1
          Points: 3 (3 x General Score)

          Draw 
        """
        player = PlayerFactory()
        game = GameFactory(owner = player, classic = True)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)

        fixture = FixtureFactory(is_finished = True)

        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_exact_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(3, fixture_points)


    def test_player_general_prediction_points_A(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 3 (3 x General Score)

          Wins local
        """
        player = PlayerFactory()
        game = GameFactory(owner = player, classic = True)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 1)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals + 1,
                                           local_team_goals = match.local_team_goals + 1)

        self.assertTrue(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(3, fixture_points)

    def test_player_general_prediction_points_B(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 3 (3 x General Score)

          Wins Visitor
        """
        player = PlayerFactory()
        game = GameFactory(owner = player, classic = True)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 1, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals + 1,
                                           local_team_goals = match.local_team_goals + 1)

        self.assertTrue(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(3, fixture_points)

    def test_player_general_prediction_points_C(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 3 (3 x General Score)

          Draw 
        """
        player = PlayerFactory()
        game = GameFactory(owner = player, classic = True)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = match.visitor_team_goals + 1,
                                           local_team_goals = match.local_team_goals + 1)

        self.assertTrue(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(3, fixture_points)

    def test_player_bad_prediction_points_A(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0 (0 x General Score)

          Bad prediction
        """
        player = PlayerFactory()
        game = GameFactory(owner = player, classic = True)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 1, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 1)

        self.assertFalse(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)

    def test_player_bad_prediction_points_B(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0 (0 x General Score)

          Bad prediction
        """
        player = PlayerFactory()
        game = GameFactory(owner = player, classic = True)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 1)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 1,
                                           local_team_goals = 0)

        self.assertFalse(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)

    def test_player_bad_prediction_points_C(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0 (0 x General Score)

          Bad prediction
        """
        player = PlayerFactory()
        game = GameFactory(owner = player, classic = True)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 1,
                                           local_team_goals = 0)

        self.assertFalse(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)

    def test_player_bad_prediction_points_D(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0 (0 x General Score)

          Bad prediction
        """
        player = PlayerFactory()
        game = GameFactory(owner = player, classic = True)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 1)

        self.assertFalse(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)

    def test_player_match_not_finished_points_A(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0 (0 x General Score)

          Match is not finished: general prediction
        """
        player = PlayerFactory()
        game = GameFactory(owner = player, classic = True)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = False, visitor_team_goals = 0, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 1,
                                           local_team_goals = 1)

        self.assertFalse(match_prediction.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)

    def test_player_match_not_finished_points_B(self):
        """ 
          Match: 1
          Predictions: 1 
          Predictions with points: 1
          Points: 0 (0 x General Score)

          Match is not finished: exact prediction
        """
        player = PlayerFactory()
        game = GameFactory(owner = player, classic = True)
        gameplayer = GamePlayerFactory(game = game, player = player, status = True)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_finished = False, visitor_team_goals = 1, local_team_goals = 0)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 1,
                                           local_team_goals = 0)

        self.assertFalse(match_prediction.is_exact_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(0, fixture_points)


    def test_multiples_predictions(self):
        fixture = FixtureFactory(is_finished = True)
        player = PlayerFactory()
        game = GameFactory(classic = True, owner = player)
        gameplayer = GamePlayerFactory(player = player, game = game, status = True)
        # Prediction ok
        match = MatchFactory(fixture = fixture,
                             is_classic = True, 
                             is_finished = True,
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
                             is_finished = True,
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
                             is_finished = True,
                             local_team_goals = 0) 
        player_prediction_2 = \
                PlayerMatchPredictionFactory(match = match_2,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 2,
                                           local_team_goals = 2)

        self.assertTrue(player_prediction.is_general_prediction())
        self.assertFalse(player_prediction_1.is_general_prediction())
        self.assertTrue(player_prediction_2.is_general_prediction())
        fixture_points = gameplayer.get_fixture_points(match.fixture)[0]
        self.assertEqual(10, fixture_points)

    def test_fixture_points(self):
        game = GameFactory(classic = True)
        player = PlayerFactory()
        game = GameFactory(classic = True, owner = player)
        gameplayer = GamePlayerFactory(player = player, game = game, status = True)
        fixture = FixtureFactory(is_finished = True)
        fixture_2 = FixtureFactory(tournament = fixture.tournament, is_finished = True)



        # Prediction ok: 2 classic, 3 prediction: 5 points
        # Fixture 1
        match = MatchFactory(is_classic = True, 
                             fixture = fixture,
                             visitor_team_goals = 2,
                             is_finished = True,
                             local_team_goals = 0) 
        player_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 3,
                                           local_team_goals = 0)

        # Prediction ok: 2 classic, 3 prediction: 5 points
        match_1 = MatchFactory(is_classic = True, 
                             fixture = fixture,
                             is_finished = True,
                             visitor_team_goals = 2,
                             local_team_goals = 0) 
        player_prediction_1 = \
                PlayerMatchPredictionFactory(match = match_1,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 2,
                                           local_team_goals = 0)

        # Prediction ok: 2 classic, 3 prediction: 5 points
        match_2 = MatchFactory(fixture = fixture_2,
                             is_classic = True, 
                             is_finished = True,
                             visitor_team_goals = 0,
                             local_team_goals = 0) 
        player_prediction_2 = \
                PlayerMatchPredictionFactory(match = match_2,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 2,
                                           local_team_goals = 2)

        # Fixture 2
        # Match suspended
        match_3 = MatchFactory(fixture = fixture_2,
                             is_classic = True, 
                             is_finished = False,
                             visitor_team_goals = 0,
                             local_team_goals = 0) 

        player_prediction_3 = \
                PlayerMatchPredictionFactory(match = match_3,
                                           gameplayer = gameplayer,
                                           visitor_team_goals = 0,
                                           local_team_goals = 0)

        fixture_points = gameplayer.get_fixture_points(fixture)[0]
        self.assertEqual(10, fixture_points)

        fixture2_points = gameplayer.get_fixture_points(fixture_2)[0]
        self.assertEqual(5, fixture2_points)

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

        self.assertEqual(2, len(gp.get_fixture_predictions(fixture_1)))
        self.assertFalse(gp.get_fixture_predictions(fixture_2))

class FixturePointsTest(TestCase):
    def test_calculate_fixture_points_A(self):
        """
          We test if when a Fixture is finished the points are calculated correctly

          The player gets 6 points from an Exact Prediction
        """
        gp = GamePlayerFactory(status = True) # The game is an Exact Game

        fixture = FixtureFactory(tournament = gp.game.tournament)

        # Match is finished so we can count the points
        match = MatchFactory(fixture = fixture, is_finished = True) 

        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = match.visitor_team_goals,
                                    local_team_goals = match.local_team_goals)

        fixture.is_finished = True
        fixture.save()

        self.assertTrue(FixturePlayerPoints.objects.first())
        self.assertEqual(FixturePlayerPoints.objects.first().points, 6)

    def test_calculate_fixture_points_B(self):
        """
          We test if when a Fixture is finished the points are calculated correctly

          The player gets 3 points from a General Prediction
        """
        gp = GamePlayerFactory(status = True) # The game is an Exact Game

        fixture = FixtureFactory(tournament = gp.game.tournament)

        # Match is finished so we can count the points
        match = MatchFactory(fixture = fixture, is_finished = True) 

        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = match.visitor_team_goals + 1,
                                    local_team_goals = match.local_team_goals + 1)

        fixture.is_finished = True
        fixture.save()

        self.assertTrue(FixturePlayerPoints.objects.first())
        self.assertEqual(FixturePlayerPoints.objects.first().points, 3)


    def test_calculate_fixture_points_C(self):
        """
          We test if when a Fixture is finished the points are calculated correctly

          The player gets 0 points from a Bad Prediction
        """
        gp = GamePlayerFactory(status = True) # The game is an Exact Game

        fixture = FixtureFactory(tournament = gp.game.tournament)

        # Match is finished so we can count the points
        match = MatchFactory(fixture = fixture, is_finished = True,
                            visitor_team_goals = 0, local_team_goals = 0) 

        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = 1,
                                    local_team_goals = 0)

        fixture.is_finished = True
        fixture.save()

        self.assertTrue(FixturePlayerPoints.objects.first())
        self.assertEqual(FixturePlayerPoints.objects.first().points, 0)

    def test_calculate_fixture_points_D(self):
        """
          We test if when a Fixture is finished the points are calculated correctly

          The player gets 0 points from an Unfinished Match
        """
        gp = GamePlayerFactory(status = True) # The game is an Exact Game

        fixture = FixtureFactory(tournament = gp.game.tournament)

        # Match is finished so we can count the points
        match = MatchFactory(fixture = fixture) 

        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = match.visitor_team_goals,
                                    local_team_goals = match.local_team_goals)

        fixture.is_finished = True
        fixture.save()

        self.assertTrue(FixturePlayerPoints.objects.first())
        self.assertEqual(FixturePlayerPoints.objects.first().points, 0)

    def test_calculate_fixture_points_with_three_matches(self):
        """
          We test if when a Fixture is finished the points are calculated correctly

          The player gets 0 points from an Match 1
          The player gets 3 points from an Match 2
          The player gets 6 points from an Match 3
        """
        gp = GamePlayerFactory(status = True) # The game is an Exact Game

        fixture = FixtureFactory(tournament = gp.game.tournament)

        # Match is finished so we can count the points
        match_1 = MatchFactory(fixture = fixture, is_finished = True, visitor_team_goals = 0, local_team_goals = 0) 
        match_2 = MatchFactory(fixture = fixture, is_finished = True) 
        match_3 = MatchFactory(fixture = fixture, is_finished = True) 


        # 0 Points
        PlayerMatchPredictionFactory(match = match_1, 
                                    gameplayer = gp,
                                    visitor_team_goals = 1,
                                    local_team_goals = 0)

        # 3 Points
        PlayerMatchPredictionFactory(match = match_2, 
                                    gameplayer = gp,
                                    visitor_team_goals = match_2.visitor_team_goals + 1,
                                    local_team_goals = match_2.local_team_goals + 1)

        # 6 Points
        PlayerMatchPredictionFactory(match = match_3, 
                                    gameplayer = gp,
                                    visitor_team_goals = match_3.visitor_team_goals,
                                    local_team_goals = match_3.local_team_goals)

        fixture.is_finished = True
        fixture.save()

        self.assertEqual(FixturePlayerPoints.objects.first().points, 9)
      
    def test_calculate_fixture_is_saved_twice(self):
        """
          We test if when a Fixture is saves twice we only has a FixturePlayerPoints
        """
        gp = GamePlayerFactory(status = True) # The game is an Exact Game

        fixture = FixtureFactory(tournament = gp.game.tournament)

        # Match is finished so we can count the points
        match = MatchFactory(fixture = fixture, is_finished = True) 

        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = match.visitor_team_goals,
                                    local_team_goals = match.local_team_goals)

        fixture.is_finished = True
        fixture.save()
        fixture.save()

        self.assertEqual(FixturePlayerPoints.objects.all().count(), 1)

    def test_calculate_fixture_points_classic_match_A(self):
        """
          We test if when a Fixture is finished the points are calculated correctly

          The player predicts correctly the classic in a Classic game
        """
        game = GameFactory(classic = True)
        gp = GamePlayerFactory(status = True, game = game) 

        fixture = FixtureFactory(tournament = gp.game.tournament)

        # Match is finished so we can count the points
        # 3 points
        match = MatchFactory(fixture = fixture, is_finished = True) 
        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = match.visitor_team_goals + 1,
                                    local_team_goals = match.local_team_goals + 1)


        # 5 points because it's a classic match
        match = MatchFactory(fixture = fixture, is_finished = True, is_classic = True) 
        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = match.visitor_team_goals,
                                    local_team_goals = match.local_team_goals)

        fixture.is_finished = True
        fixture.save()

        self.assertTrue(FixturePlayerPoints.objects.first())
        self.assertEqual(FixturePlayerPoints.objects.first().points, 8)
        self.assertTrue(FixturePlayerPoints.objects.first().classic_prediction)

    def test_calculate_fixture_points_classic_match_B(self):
        """
          We test if when a Fixture is finished the points are calculated correctly

          The player does not predicts correctly the classic in a Classic game
        """
        game = GameFactory(classic = True)
        gp = GamePlayerFactory(status = True, game = game) 

        fixture = FixtureFactory(tournament = gp.game.tournament)

        # Match is finished so we can count the points
        # 3 points
        match = MatchFactory(fixture = fixture, is_finished = True) 
        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = match.visitor_team_goals + 1,
                                    local_team_goals = match.local_team_goals + 1)


        # 0 points
        match = MatchFactory(fixture = fixture, is_finished = True, is_classic = True, visitor_team_goals = 0, local_team_goals = 0) 
        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = 1,
                                    local_team_goals = 0)

        fixture.is_finished = True
        fixture.save()

        self.assertTrue(FixturePlayerPoints.objects.first())
        self.assertEqual(FixturePlayerPoints.objects.first().points, 3)
        self.assertFalse(FixturePlayerPoints.objects.first().classic_prediction)

    def test_calculate_fixture_points_classic_match_C(self):
        """
          We test if when a Fixture is finished the points are calculated correctly

          The player predicts correctly the classic in an Exact game
        """
        gp = GamePlayerFactory(status = True) 

        fixture = FixtureFactory(tournament = gp.game.tournament)

        # Match is finished so we can count the points
        # 3 points
        match = MatchFactory(fixture = fixture, is_finished = True) 
        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = match.visitor_team_goals + 1,
                                    local_team_goals = match.local_team_goals + 1)


        # 8 points because it's a classic match, 3 because it is an exact prediction, 3 because it is a general prediction
        match = MatchFactory(fixture = fixture, is_finished = True, is_classic = True) 
        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = match.visitor_team_goals,
                                    local_team_goals = match.local_team_goals)

        fixture.is_finished = True
        fixture.save()

        self.assertTrue(FixturePlayerPoints.objects.first())
        self.assertEqual(FixturePlayerPoints.objects.first().points, 11)
        self.assertTrue(FixturePlayerPoints.objects.first().classic_prediction)

    def test_calculate_fixture_points_classic_match_D(self):
        """
          We test if when a Fixture is finished the points are calculated correctly

          The player predicts correctly the classic in an Exact game
        """
        gp = GamePlayerFactory(status = True) 

        fixture = FixtureFactory(tournament = gp.game.tournament)

        # Match is finished so we can count the points
        # 3 points
        match = MatchFactory(fixture = fixture, is_finished = True) 
        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = match.visitor_team_goals + 1,
                                    local_team_goals = match.local_team_goals + 1)


        # 5 because it is a general prediction and a classic
        match = MatchFactory(fixture = fixture, is_finished = True, is_classic = True) 
        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = match.visitor_team_goals + 1,
                                    local_team_goals = match.local_team_goals + 1)

        fixture.is_finished = True
        fixture.save()

        self.assertTrue(FixturePlayerPoints.objects.first())
        self.assertEqual(FixturePlayerPoints.objects.first().points, 8)
        self.assertTrue(FixturePlayerPoints.objects.first().classic_prediction)

    def test_calculate_fixture_points_classic_match_E(self):
        """
          We test if when a Fixture is finished the points are calculated correctly

          The player does not predicts correctly the classic in an Exact game
        """
        gp = GamePlayerFactory(status = True) 

        fixture = FixtureFactory(tournament = gp.game.tournament)

        # Match is finished so we can count the points
        # 3 points
        match = MatchFactory(fixture = fixture, is_finished = True) 
        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = match.visitor_team_goals + 1,
                                    local_team_goals = match.local_team_goals + 1)


        # 0 points
        match = MatchFactory(fixture = fixture, is_finished = True, is_classic = True, visitor_team_goals = 0, local_team_goals = 0) 
        PlayerMatchPredictionFactory(match = match, 
                                    gameplayer = gp,
                                    visitor_team_goals = 1,
                                    local_team_goals = 0)

        fixture.is_finished = True
        fixture.save()

        self.assertTrue(FixturePlayerPoints.objects.first())
        self.assertEqual(FixturePlayerPoints.objects.first().points, 3)
        self.assertFalse(FixturePlayerPoints.objects.first().classic_prediction)
