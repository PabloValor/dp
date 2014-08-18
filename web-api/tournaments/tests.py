import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from games.factories import * # Circular
from .factories import *

class TournamentAPITest(APITestCase):
    def test_get_200_OK(self):
        tournament_1 = TournamentFactory()
        tournament_2 = TournamentFactory()
        player = PlayerFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        url = reverse('tournamentList')
        response = self.client.get(url)
        r_tournaments = json.loads(response.content)

        self.assertEqual(len(r_tournaments), 2)
        self.assertEqual(r_tournaments[0]['name'], tournament_1.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_401_UNAUTHORIZED(self):
        tournament_1 = TournamentFactory()

        url = reverse('tournamentList')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tournament_with_teams_200_OK(self):
        # Tournament
        tournament = TournamentFactory()
        fixture = FixtureFactory(tournament = tournament)
        team_1 = TeamFactory()
        team_2 = TeamFactory()
        match = MatchFactory(local_team = team_1, visitor_team = team_2, fixture = fixture)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player asks for the tournament
        url = reverse('tournamentList')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]['teams']), 2)

class TournamentFixtureAPITest(APITestCase):
    def test_get_tournament_fixtures_200_OK(self):
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Assert
        self.assertEqual(len(response.data['fixtures']), 3)
        self.assertEqual(response.data['fixtures'][0]['number'], fixture_1.number)
        self.assertEqual(response.data['fixtures'][1]['number'], fixture_2.number)
        self.assertEqual(response.data['fixtures'][2]['number'], fixture_3.number)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_multiples_tournament_fixtures_200_OK(self):
        """ 
            We test from multiples tournaments to see 
            if the filters works 
        """
        # Tournament 
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Tournament B
        tournament_b = TournamentFactory()
        FixtureFactory(tournament = tournament_b, number = 0)
        FixtureFactory(tournament = tournament_b, number = 1)

        # Tournament C
        tournament_c = TournamentFactory()
        FixtureFactory(tournament = tournament_c, number = 0)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Tournament A
        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Assert 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['fixtures']), 3)
        self.assertEqual(response.data['fixtures'][0]['number'], fixture_1.number)
        self.assertEqual(response.data['fixtures'][1]['number'], fixture_2.number)
        self.assertEqual(response.data['fixtures'][2]['number'], fixture_3.number)

        # Tournament B
        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament_b.id })
        response = self.client.get(url)

        # Assert 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['fixtures']), 2)

        # Tournament C
        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament_c.id })
        response = self.client.get(url)

        # Assert 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['fixtures']), 1)

    def test_get_empty_fixture_from_unexesting_tournament_404_NOT_FOUND(self):
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament.id + 1 })
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anon_gets_fixture_401_UNAUTHORIZED(self):
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0)

        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_fixture_ordered_by_number(self):
        # Tournament
        tournament = TournamentFactory()

        fixture_3 = FixtureFactory(tournament = tournament, number = 2)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_1 = FixtureFactory(tournament = tournament, number = 0)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Asset
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['fixtures'][0]['number'], fixture_1.number)
        self.assertEqual(response.data['fixtures'][1]['number'], fixture_2.number)
        self.assertEqual(response.data['fixtures'][2]['number'], fixture_3.number)

    def test_get_fixture_with_current_fixture_A(self):
        # Tournament
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Asset
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_fixture']['number'], fixture_1.number)
        self.assertFalse(response.data['is_finished'])

    def test_get_fixture_with_current_fixture_B(self):
        # Tournament
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Asset
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_fixture']['number'], fixture_2.number)
        self.assertFalse(response.data['is_finished'])

    def test_get_fixture_with_current_fixture_C(self):
        # Tournament
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1, is_finished = True)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Asset
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_fixture']['number'], fixture_3.number)
        self.assertFalse(response.data['is_finished'])

    def test_get_tournament_finished(self):
        # Tournament
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1, is_finished = True)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2, is_finished = True)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Asset
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_fixture'], None)
        self.assertTrue(response.data['is_finished'])

    def test_get_fixture_with_matches(self):
        # Tournament
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        MatchFactory(fixture = fixture_1)
        MatchFactory(fixture = fixture_1)
        MatchFactory(fixture = fixture_1)

        fixture_2 = FixtureFactory(tournament = tournament, number = 1, is_finished = True)
        MatchFactory(fixture = fixture_2)
        MatchFactory(fixture = fixture_2)

        fixture_3 = FixtureFactory(tournament = tournament, number = 2)
        MatchFactory(fixture = fixture_3)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Asset
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['fixtures'][0]['matches']), 3)
        self.assertEqual(len(response.data['fixtures'][1]['matches']), 2)
        self.assertEqual(len(response.data['fixtures'][2]['matches']), 1)

    def test_get_fixture_with_detailed_matches(self):
        # Tournament
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        match_1 = MatchFactory(fixture = fixture_1)
        match_2 = MatchFactory(fixture = fixture_1)
        match_3 = MatchFactory(fixture = fixture_1)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentFixtureList', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Asset
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['fixtures'][0]['matches']), 3)

        self.assertEqual(response.data['fixtures'][0]['matches'][0]['date'], match_1.date)
        self.assertEqual(response.data['fixtures'][0]['matches'][0]['local_team']['name'], match_1.local_team.name)
        self.assertEqual(response.data['fixtures'][0]['matches'][0]['visitor_team']['name'], match_1.visitor_team.name)

        self.assertEqual(response.data['fixtures'][0]['matches'][1]['date'], match_2.date)
        self.assertEqual(response.data['fixtures'][0]['matches'][1]['local_team']['name'], match_2.local_team.name)
        self.assertEqual(response.data['fixtures'][0]['matches'][1]['visitor_team']['name'], match_2.visitor_team.name)

        self.assertEqual(response.data['fixtures'][0]['matches'][2]['date'], match_3.date)
        self.assertEqual(response.data['fixtures'][0]['matches'][2]['local_team']['name'], match_3.local_team.name)
        self.assertEqual(response.data['fixtures'][0]['matches'][2]['visitor_team']['name'], match_3.visitor_team.name)

class FixtureTest(TestCase):
    def test_get_active_fixture_A(self):
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        self.assertEqual(tournament.get_current_fixture(), fixture_1)

    def test_get_active_fixture_B(self):
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, is_finished = True, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        self.assertEqual(tournament.get_current_fixture(), fixture_2)

    def test_get_active_fixture_C(self):
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, is_finished = True, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, is_finished = True, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        self.assertEqual(tournament.get_current_fixture(), fixture_3)

    def test_get_past_fixtures_A(self):
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        self.assertEqual(tournament.get_past_fixtures().count(), 0)

    def test_get_past_fixtures_B(self):
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, is_finished = True, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        self.assertEqual(tournament.get_past_fixtures().count(), 1)

    def test_get_past_fixtures_C(self):
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, is_finished = True, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, is_finished = True, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        self.assertEqual(tournament.get_past_fixtures().count(), 2)

    def test_get_past_fixtures_D(self):
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, is_finished = True, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, is_finished = True, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, is_finished = True, number = 2)

        self.assertEqual(tournament.get_past_fixtures().count(), 3)

    def test_get_future_fixtures_A(self):
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        self.assertEqual(tournament.get_future_fixtures().count(), 3)

    def test_get_future_fixtures_B(self):
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        self.assertEqual(tournament.get_future_fixtures().count(), 2)

    def test_get_future_fixtures_C(self):
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1, is_finished = True)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        self.assertEqual(tournament.get_future_fixtures().count(), 1)

    def test_get_future_fixtures_C(self):
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1, is_finished = True)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2, is_finished = True)

        self.assertEqual(tournament.get_future_fixtures().count(), 0)

class TournamentTest(TestCase):
    def test_get_tournament_teams(self):
        # Tournament
        tournament = TournamentFactory()
        fixture = FixtureFactory(tournament = tournament)
        team_1 = TeamFactory()
        team_2 = TeamFactory()
        match = MatchFactory(local_team = team_1, visitor_team = team_2, fixture = fixture)

        teams = tournament.get_teams()
        self.assertEqual(len(teams), 2)
