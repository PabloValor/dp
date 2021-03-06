import json
import random
from django.utils import timezone
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
        tournament.teams.add(team_1)
        tournament.teams.add(team_2)        
        match = MatchFactory(local_team = team_1, visitor_team = team_2, fixture = fixture)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player asks for the tournament
        url = reverse('tournamentTeamsList')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]['teams']), 2)

    def test_get_401_UNAUTHORIZED(self):
        tournament_1 = TournamentFactory()

        url = reverse('tournamentTeamsList')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)        

    def test_get_tournament_with_teams_stats_200_OK(self):
        # Tournament
        tournament = TournamentFactory()
        fixture = FixtureFactory(tournament = tournament)
        local_team = TeamFactory()
        visitor_team = TeamFactory()        
        tournament.teams.add(local_team)
        tournament.teams.add(visitor_team)        
        match = MatchFactory(local_team = local_team, visitor_team = visitor_team,
                             fixture = fixture, is_finished = True,
                             local_team_goals = 1, visitor_team_goals = 0)
        
        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player asks for the tournament with stats
        url = reverse('tournamentStats', kwargs = {'pk': tournament.id })        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        teams = response.data['teams']

        # Order by ID reverse
        team = teams[1]
        self.assertEqual(team['stats']['w'], 0)
        self.assertEqual(team['stats']['d'], 0)
        self.assertEqual(team['stats']['l'], 1)

        team = teams[0]
        self.assertEqual(team['stats']['w'], 1)
        self.assertEqual(team['stats']['d'], 0)
        self.assertEqual(team['stats']['l'], 0)        

    def test_get_tournament_with_teams_stats_401_UNAUTHORIZED(self):
        tournament = TournamentFactory()

        url = reverse('tournamentStats', kwargs = {'pk': tournament.id })                
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
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
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['fixtures']), 3)
        self.assertEqual(response.data['fixtures'][0]['number'], fixture_1.number)
        self.assertEqual(response.data['fixtures'][1]['number'], fixture_2.number)
        self.assertEqual(response.data['fixtures'][2]['number'], fixture_3.number)

        # Tournament B
        # Player gets Tournament Fixture
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament_b.id })
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['fixtures']), 2)

        # Tournament C
        # Player gets Tournament Fixture
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament_c.id })
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
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id + 1 })
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anon_gets_fixture_401_UNAUTHORIZED(self):
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0)

        # Player gets Tournament Fixture
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
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
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
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
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
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
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
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
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Asset
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_fixture']['number'], fixture_3.number)
        self.assertFalse(response.data['is_finished'])

    def test_get_tournament_finished(self):
        # Tournament
        tournament = TournamentFactory(is_finished = True)

        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
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
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
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
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['fixtures'][0]['matches']), 3)

        self.assertEqual(response.data['fixtures'][0]['matches'][0]['date'], str(match_1.date))
        self.assertEqual(response.data['fixtures'][0]['matches'][0]['local_team']['name'], match_1.local_team.name)
        self.assertEqual(response.data['fixtures'][0]['matches'][0]['visitor_team']['name'], match_1.visitor_team.name)

        self.assertEqual(response.data['fixtures'][0]['matches'][1]['date'], str(match_2.date))
        self.assertEqual(response.data['fixtures'][0]['matches'][1]['local_team']['name'], match_2.local_team.name)
        self.assertEqual(response.data['fixtures'][0]['matches'][1]['visitor_team']['name'], match_2.visitor_team.name)

        self.assertEqual(response.data['fixtures'][0]['matches'][2]['date'], str(match_3.date))
        self.assertEqual(response.data['fixtures'][0]['matches'][2]['local_team']['name'], match_3.local_team.name)
        self.assertEqual(response.data['fixtures'][0]['matches'][2]['visitor_team']['name'], match_3.visitor_team.name)

    def test_get_fixture_with_finished_matches(self):
        # Tournament
        tournament = TournamentFactory()

        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        match_1 = MatchFactory(fixture = fixture_1, is_finished = True)
        match_2 = MatchFactory(fixture = fixture_1)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['fixtures'][0]['matches'][0]['is_finished'])
        self.assertFalse(response.data['fixtures'][0]['matches'][1]['is_finished'])

    def test_get_fixture_with_its_playing_info_A(self):
        # Tournament
        tournament = TournamentFactory()
        fixture = FixtureFactory(tournament = tournament, open_until = timezone.now())

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Asset
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['fixtures'][0]['is_closed'])

    def test_get_fixture_with_its_playing_info_B(self):
        # Tournament
        tournament = TournamentFactory()
        fixture = FixtureFactory(tournament = tournament)
        
        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets Tournament Fixture
        url = reverse('tournamentAllFixtures', kwargs = {'pk': tournament.id })
        response = self.client.get(url)

        # Asset
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['fixtures'][0]['is_closed'])

    def test_get_tournaments_next_fixture_200_OK_A(self):
        """
        We get next fixture from all the tournaments of the site.
        Tournaments: 1

        Tournament only has one Fixture. Next is None.
        """
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Current Fixture
        url = reverse('allTournamentNextFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['fixture'], None)        

    def test_get_tournaments_next_fixture_200_OK_B(self):
        """
        We get next fixture from all the tournaments of the site.
        Tournaments: 1

        Tournament  has began. Next fixture is fixture_2
        """        
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Next Fixture
        url = reverse('allTournamentNextFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], fixture_2.number)


    def test_get_tournaments_next_fixture_200_OK_C(self):
        """
        We get next fixture from all the tournaments of the site.
        Tournaments: 1

        Tournament  has began. Next fixture is fixture_3
        """                
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1, is_finished = True)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Next Fixture
        url = reverse('allTournamentNextFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], fixture_3.number)

    def test_get_tournaments_next_fixture_200_OK_D(self):
        """
        We get next fixture from all the tournaments of the site.
        Tournaments: 1

        Tournament has finished. There are no more fixtures to be play.
        """                        
        # Tournament
        tournament = TournamentFactory(is_finished = True)
        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Next Fixture
        url = reverse('allTournamentNextFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 0)

    def test_get_tournaments_next_fixture_200_OK_E(self):
        """
        We get next fixture from all the tournaments of the site.

        Tournaments: 3
        """                                
        # Tournament
        tournament = TournamentFactory()
        FixtureFactory(tournament = tournament, is_finished = True, number = 1)
        FixtureFactory(tournament = tournament, number = 2)        

        # Tournament B
        tournament_b = TournamentFactory()
        FixtureFactory(tournament = tournament_b, is_finished = True, number = 3 )        
        FixtureFactory(tournament = tournament_b, number = 4)

        # Tournament C
        tournament_c = TournamentFactory()
        FixtureFactory(tournament = tournament_c, is_finished = True, number = 5 )        
        FixtureFactory(tournament = tournament_c, number = 6)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Tournament A
        # Player gets Tournament Fixture
        url = reverse('allTournamentNextFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], 2)
        
        self.assertEqual(response.data[1]['tournament_name'], tournament_b.name)
        self.assertEqual(response.data[1]['fixture']['number'], 4)
        
        self.assertEqual(response.data[2]['tournament_name'], tournament_c.name)
        self.assertEqual(response.data[2]['fixture']['number'], 6)

    def test_get_tournaments_next_fixture_200_OK_F(self):
        """
        We get next fixture from all the tournaments of the site.
        Tournaments: 1

        Tournament isn't started. Next fixture is fixture_2.
        This is an exception to the rule.
        """
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Next Fixture
        url = reverse('allTournamentNextFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], fixture_2.number)

    def test_get_tournaments_next_fixture_when_there_is_one_playing_200_OK_A(self):
        """
        We get next fixture from all the tournaments of the site.
        Tournaments: 1

        If a fixture is being played we get the next one.
        """
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_playing = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Next Fixture
        url = reverse('allTournamentNextFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], fixture_2.number)

    def test_get_tournaments_next_fixture_when_there_is_one_playing_200_OK_B(self):
        """
        We get next fixture from all the tournaments of the site.
        Tournaments: 1

        If a fixture is being played we get the next one.
        """
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1, is_playing = True)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Next Fixture
        url = reverse('allTournamentNextFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], fixture_3.number)        


    def test_get_tournaments_next_fixture_when_there_is_one_playing_200_OK_C(self):
        """
        We get next fixture from all the tournaments of the site.
        Tournaments: 1

        If a fixture is being played we get the next one.
        """
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1, is_playing = True, is_finished = True)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Next Fixture
        url = reverse('allTournamentNextFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], fixture_3.number)

    def test_get_tournaments_next_fixture_when_there_is_one_playing_200_OK_D(self):
        """
        We get next fixture from all the tournaments of the site.
        Tournaments: 1

        Tournament is playing his last fixture. 
        """
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1, is_playing = True, is_finished = True)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2, is_playing = True)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Next Fixture
        url = reverse('allTournamentNextFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['fixture'], None)        

    def test_get_tournaments_current_or_last_fixture_200_OK_A(self):
        """
        We get the current or last fixture from all the tournaments of the site.
        Tournaments: 1

        Tournament hasn't started. Current fixture is the first.
        """
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Current Fixture
        url = reverse('allTournamentCurrentOrLastFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], fixture_1.number)

    def test_get_tournaments_current_or_last_fixture_200_OK_B(self):
        """
        We get the current or last fixture from all the tournaments of the site.
        Tournaments: 1
        Is Playing: True

        Tournament has started. The first fixture is being playing so the 
         Current fixture is still the first fixture.
        """
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_playing = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Current Fixture
        url = reverse('allTournamentCurrentOrLastFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], fixture_1.number)

        
    def test_get_tournaments_current_or_last_fixture_200_OK_C(self):
        """
        We get the current or last fixture from all the tournaments of the site.
        Tournaments: 1
        Is Playing: True

        Tournament has started. The first fixture has finished so it's the last fixture.
        """
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_playing = True, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Current Fixture
        url = reverse('allTournamentCurrentOrLastFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], fixture_1.number)

    def test_get_tournaments_current_or_last_fixture_200_OK_D(self):
        """
        We get the current or last fixture from all the tournaments of the site.
        Tournaments: 1
        Is Playing: True

        Tournament is playing his last fixture.
        Current Fixture: fixture_3
        """
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_playing = True, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1, is_finished = True)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2, is_playing = True)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Current Fixture
        url = reverse('allTournamentCurrentOrLastFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], fixture_3.number)

    def test_get_tournaments_current_or_last_fixture_200_OK_DA(self):
        """
        We get the current or last fixture from all the tournaments of the site.
        Tournaments: 1
        Is Playing: False

        Tournament is playing his last fixture.
        Current Fixture: fixture_2
        """
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_playing = True, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1, is_finished = True)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Current Fixture
        url = reverse('allTournamentCurrentOrLastFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], fixture_2.number)        


    def test_get_tournaments_current_or_last_fixture_200_OK_E(self):
        """
        We get the current or last fixture from all the tournaments of the site.
        Tournaments: 1
        Is Playing: True

        Tournament has finished
        Current Fixture is the last one.
        """
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0, is_playing = True, is_finished = True)
        fixture_2 = FixtureFactory(tournament = tournament, number = 1, is_finished = True)
        fixture_3 = FixtureFactory(tournament = tournament, number = 2, is_playing = True, is_finished = True)

        # Player
        player = PlayerFactory()
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        # Player gets from All the Tournaments the Current Fixture
        url = reverse('allTournamentCurrentOrLastFixtureList')
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tournament_name'], tournament.name)
        self.assertEqual(response.data[0]['fixture']['number'], fixture_3.number)                        

    def test_get_tournament_fixture_by_id_200_OK(self):
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
        url = reverse('tournamentFixture', kwargs = {'pk': fixture_2.id })
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.data['number'], fixture_2.number)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anon_get_tournament_401_UNAUTHORIZED(self):
        # Tournament
        tournament = TournamentFactory()
        fixture_1 = FixtureFactory(tournament = tournament, number = 0)

        # Player gets Tournament Fixture
        url = reverse('tournamentFixture', kwargs = {'pk': fixture_1.id })
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tournament_fixture_by_number_A_200_OK(self):
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
        url = reverse('tournamentFixtureByNumber', kwargs = {'pk': tournament.id, 'number': fixture_2.number })
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.data['number'], fixture_2.number)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tournament_fixture_by_number_B_200_OK(self):
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
        url = reverse('tournamentFixtureByNumber', kwargs = {'pk': tournament.id, 'number': fixture_3.number })
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.data['number'], fixture_3.number)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        tournament.teams.add(team_1)
        tournament.teams.add(team_2)
        teams = tournament.teams.all()
        self.assertEqual(len(teams), 2)


    def test_get_all_finished_matches_1(self):
        """
        Test Get all finished matches' team
        """
        
        tournament = TournamentFactory()
        fixture = FixtureFactory(tournament = tournament)
        team = TeamFactory()        
        match = MatchFactory(local_team = team, fixture = fixture, is_finished = True)        

        matches = team.get_all_finished_matches(tournament)

        self.assertEqual(matches[0], match)

    def test_get_all_finished_matches_2(self):
        """
        Test Get all finished matches' team
        """
        
        tournament = TournamentFactory()
        fixture = FixtureFactory(tournament = tournament)
        team = TeamFactory()        
        match_1 = MatchFactory(local_team = team, fixture = fixture, is_finished = True)
        match_2 = MatchFactory(local_team = team, fixture = fixture, is_finished = True)                

        matches = team.get_all_finished_matches(tournament)

        self.assertEqual(matches[0], match_1)
        self.assertEqual(matches[1], match_2)        
        
    def test_get_tournament_stats_1(self):
        """
        Test Local teams stats.
        
        Stats: W:1 D:0 L:0
        """
        tournament = TournamentFactory()
        fixture = FixtureFactory(tournament = tournament)
        team = TeamFactory()        
        match = MatchFactory(local_team = team,
                             fixture = fixture,
                             local_team_goals = 1,
                             visitor_team_goals = 0,
                             is_finished = True)

        stats = team.get_tournament_stats(tournament)
        self.assertEqual(stats['w'], 1)
        self.assertEqual(stats['d'], 0)
        self.assertEqual(stats['l'], 0)

    def test_get_tournament_stats_2(self):
        """
        Test Local teams stats.
        
        Stats: W:0 D:1 L:0
        """
        tournament = TournamentFactory()
        fixture = FixtureFactory(tournament = tournament)
        team = TeamFactory()        
        match = MatchFactory(local_team = team,
                             fixture = fixture,
                             local_team_goals = 1,
                             visitor_team_goals = 1,
                             is_finished = True)

        stats = team.get_tournament_stats(tournament)
        self.assertEqual(stats['w'], 0)
        self.assertEqual(stats['d'], 1)
        self.assertEqual(stats['l'], 0)

    def test_get_tournament_stats_3(self):
        """
        Test Local teams stats.
        
        Stats: W:0 D:0 L:1
        """
        tournament = TournamentFactory()
        fixture = FixtureFactory(tournament = tournament)
        team = TeamFactory()        
        match = MatchFactory(local_team = team,
                             fixture = fixture,
                             local_team_goals = 0,
                             visitor_team_goals = 1, 
                             is_finished = True)

        stats = team.get_tournament_stats(tournament)
        self.assertEqual(stats['w'], 0)
        self.assertEqual(stats['d'], 0)
        self.assertEqual(stats['l'], 1)

    def test_get_tournament_stats_unfinished_match_1(self):
        """
        Test Unfinished Game
        """
        tournament = TournamentFactory()
        fixture = FixtureFactory(tournament = tournament)
        team = TeamFactory()        
        match = MatchFactory(local_team = team,
                             fixture = fixture,
                             local_team_goals = 1,
                             visitor_team_goals = 0)

        stats = team.get_tournament_stats(tournament)
        self.assertEqual(stats['w'], 0)
        self.assertEqual(stats['d'], 0)
        self.assertEqual(stats['l'], 0)

    def test_get_tournament_stats_multiples_matches(self):
        """
        Test Local teams stats.
        """
        tournament = TournamentFactory()
        fixture = FixtureFactory(tournament = tournament)
        team = TeamFactory()

        wins = [MatchFactory(local_team = team, fixture = fixture,local_team_goals = 2, visitor_team_goals = 1, is_finished = True)
                for x in xrange(random.randint(0, 10))]

        draws = [MatchFactory(local_team = team, fixture = fixture,local_team_goals = 2, visitor_team_goals = 2, is_finished = True)
                 for x in xrange(random.randint(0, 10))]         

        losses = [MatchFactory(local_team = team, fixture = fixture,local_team_goals = 2, visitor_team_goals = 3, is_finished = True)
                  for x in xrange(random.randint(0, 10))]         

        stats = team.get_tournament_stats(tournament)

        self.assertEqual(stats['w'], len(wins))
        self.assertEqual(stats['d'], len(draws))
        self.assertEqual(stats['l'], len(losses))
