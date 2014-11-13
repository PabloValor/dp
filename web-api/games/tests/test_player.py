import unittest
from django.test import TestCase
from ..factories import GamePlayerFactory, FixturePlayerPointsFactory, PlayerFactory

class PlayerTest(TestCase):
    """
        We test the Player's methods
    """
    def test_get_all_players_games_1(self):
        """
        Player is playing one game
        """
        gameplayer = GamePlayerFactory(status = True)
        player = gameplayer.player

        self.assertEqual(player.get_all_gameplayers().count(), 1)

    def test_get_all_players_games_2(self):
        """
        Player was invited but is not playing any game
        """
        gameplayer = GamePlayerFactory(status = False)
        player = gameplayer.player

        self.assertEqual(player.get_all_gameplayers().count(), 0)

    def test_get_all_players_games_3(self):
        """
        Player is not playing any kind of game he is a very serious person
        """
        player = PlayerFactory()

        self.assertEqual(player.get_all_gameplayers().count(), 0)

    def test_get_all_points_1(self):
        """
        Player is playing one game 
        """
        gameplayer = GamePlayerFactory(status = True)
        fixture_player_points = FixturePlayerPointsFactory(points = 10, gameplayer = gameplayer)
        player = gameplayer.player

        gameplayers = player.get_all_gameplayers()
        self.assertEqual(player.get_all_games_points(gameplayers), fixture_player_points.points)
        
    def test_get_all_points_2(self):
        """
        Player is playing two games
        """
        gameplayer = GamePlayerFactory(status = True)
        fixture_player_points = FixturePlayerPointsFactory(points = 10, gameplayer = gameplayer)
        
        player = gameplayer.player
        
        gameplayer = GamePlayerFactory(status = True, player = player)
        fixture_player_points = FixturePlayerPointsFactory(points = 15, gameplayer = gameplayer)
        
        gameplayers = player.get_all_gameplayers()
        self.assertEqual(player.get_all_games_points(gameplayers), 25)

    def test_get_all_points_3(self):
        """
        Player is playing two games but it was invited to three games and
        for testing purpose only he has points in a game he is not playing
        """
        gameplayer = GamePlayerFactory(status = True)
        fixture_player_points = FixturePlayerPointsFactory(points = 10, gameplayer = gameplayer)
        
        player = gameplayer.player
        
        gameplayer = GamePlayerFactory(status = True, player = player)
        fixture_player_points = FixturePlayerPointsFactory(points = 15, gameplayer = gameplayer)

        gameplayer = GamePlayerFactory(status = False, player = player)
        fixture_player_points = FixturePlayerPointsFactory(points = 50, gameplayer = gameplayer)
        
        gameplayers = player.get_all_gameplayers()
        self.assertEqual(player.get_all_games_points(gameplayers), 25)              







