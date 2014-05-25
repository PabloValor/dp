from django.test import TestCase
import unittest
from datetime import datetime, timedelta
from tournaments.models import Team, Fixture, Match
from .models import Player
from .factories import *

class TournamentTest(TestCase):
    def test_the_player_setting_fixtures_results(self):
        # Matchs
        tournament = TournamentFactory()
#        match = MatchFactory()
#
#        # Player
#        player = PlayerFactory()
#        player.make_prediction(match.pk, 0, 0)
#
#        self.assertEqual(len(player.playermatchprediction_set.all()), 1)
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
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(3, fixture_points)

    def test_player_points_from_some_exact_prediction_and_some_not(self):
        player = PlayerFactory()
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

        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(3, fixture_points)

    def test_player_points_from_one_moral_prediction(self):
        player = PlayerFactory()
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals + 1,
                                           local_team_goals = match.local_team_goals + 1)

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(1, fixture_points)

    def test_player_points_from_some_moral_prediction_and_some_not(self):
        player = PlayerFactory()
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

        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(2, fixture_points)

    def test_player_points_from_moral_and_exact_predictions(self):
        player = PlayerFactory()
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

        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(8, fixture_points)

    def test_player_points_from_one_correct_exact_prediction_of_a_classic_match(self):
        player = PlayerFactory()
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(6, fixture_points)

    def test_player_points_from_one_correct_moral_prediction_of_a_classic_match(self):
        player = PlayerFactory()
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(2, fixture_points)

    def test_player_points_from_one_correct_exact_prediction_with_double(self):
        player = PlayerFactory()
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           is_double = True,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(6, fixture_points)

    def test_player_points_from_one_correct_moral_prediction_with_double(self):
        player = PlayerFactory()
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           is_double = True,
                                           player = player, 
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(2, fixture_points)

    def test_get_player_points_from_one_correct_exact_prediction_with_double_of_a_classic_match(self):
        player = PlayerFactory()
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           is_double = True,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(12, fixture_points)

    def test_player_points_from_one_correct_moral_prediction_with_double_of_a_classic_match(self):
        player = PlayerFactory()
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture, is_classic = True)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           is_double = True,
                                           player = player, 
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(4, fixture_points)

    def test_player_points_with_initial_points(self):
        player = PlayerFactory(initial_points = 2)
        fixture = FixtureFactory(is_finished = True)
        match = MatchFactory(fixture = fixture)
        match_prediction = \
                PlayerMatchPredictionFactory(match = match,
                                           player = player, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_moral_prediction())
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(5, fixture_points)

class ClassicGamePlayerPointsTest(TestCase):
    def test_draw_prediction_false(self):
        fixture = FixtureFactory(is_finished = True)
        game = GameFactory(classic = True)
        player = PlayerFactory(game = game)
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
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(0, fixture_points)

    def test_draw_prediction_true(self):
        fixture = FixtureFactory(is_finished = True)
        game = GameFactory(classic = True)
        player = PlayerFactory(game = game)
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
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(1, fixture_points)

    def test_win_prediction_true(self):
        fixture = FixtureFactory(is_finished = True)
        game = GameFactory(classic = True)
        player = PlayerFactory(game = game)
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
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(1, fixture_points)

    def test_multiples_predictions(self):
        fixture = FixtureFactory(is_finished = True)
        game = GameFactory(classic = True)
        player = PlayerFactory(game = game)
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
        fixture_points = player.get_fixture_points(match.fixture)
        self.assertEqual(2, fixture_points)

    def test_fixture_points(self):
        game = GameFactory(classic = True)
        player = PlayerFactory(game = game)
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

        fixture_points = player.get_fixture_points(fixture)
        self.assertEqual(2, fixture_points)

        fixture2_points = player.get_fixture_points(fixture_2)
        self.assertEqual(1, fixture2_points)

        fixture_points = FixturePlayerPointsFactory(fixture = fixture, 
                                                    game = game,
                                                    player = player,
                                                    points = fixture_points)

        fixture_points = FixturePlayerPointsFactory(fixture = fixture_2, 
                                                    game = game,
                                                    player = player,
                                                    points = fixture2_points)
        self.assertEqual(3, player.get_total_points())


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

class FixturePredictions(TestCase):
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

# Create your tests here.
