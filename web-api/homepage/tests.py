from django.test import TestCase
from django.core.exceptions import ValidationError
from models import TournamentHomepage
from tournaments.factories import TournamentFactory
from factories import NewsFactory

class TournamentHomepageTest(TestCase):
    def test_save_tournament(self):
        tournament = TournamentFactory()
        th = TournamentHomepage()
        th.tournament = tournament
        th.save()
        
        self.assertEqual(TournamentHomepage.objects.count(), 1)

    def test_save_same_tournament_two_times(self):
        tournament = TournamentFactory()
        
        th = TournamentHomepage()
        th.tournament = tournament
        th.save()

        th = TournamentHomepage()
        th.tournament = tournament
        
        self.assertRaises(ValidationError, th.clean)
        self.assertEqual(TournamentHomepage.objects.count(), 1)        

from django.core.urlresolvers import reverse        
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from games.factories import PlayerFactory
from .factories import TournamentHomepageFactory

class TournamentHomepageAPITest(APITestCase):
    def test_get_all_tournament_homepage_200_OK(self):
        th = TournamentHomepageFactory()
        
        player = PlayerFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)
 
        url = reverse('tournamentHomepageList')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], th.tournament.id)

    def test_get_zero_tournament_homepage_200_OK(self):
        player = PlayerFactory()

        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)
 
        url = reverse('tournamentHomepageList')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 0)

    def test_get_all_tournament_homepage_401_UNAUTHORIZED(self):
        url = reverse('tournamentHomepageList')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

from .models import News
        
class NewsAPITest(APITestCase):
    def test_get_all_news_200_OK(self):
        NewsFactory()
        NewsFactory()
 
        player = PlayerFactory()
        
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)
 
        url = reverse('newsList')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_get_all_news_active_200_OK(self):
        NewsFactory()
        NewsFactory(active = False)
 
        player = PlayerFactory()
        
        token = Token.objects.get(user__username = player.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)
 
        url = reverse('newsList')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
    
    def test_get_all_news_homepage_401_UNAUTHORIZED(self):
        url = reverse('newsList')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
