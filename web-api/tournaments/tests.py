import json
from django.core.urlresolvers import reverse
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
