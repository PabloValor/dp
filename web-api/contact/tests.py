from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from games.factories import PlayerFactory


class ContactAPITest(APITestCase):
    def test_creation_contact_201_CREATED(self):
        """ 
          Nico creates a Contact
        """
        nico = PlayerFactory()
        token = Token.objects.get(user__username = nico.username)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)

        data  = {'subject': 'Subject', 'text': 'text' }
        url = reverse('contactCreate')
        response = self.client.post(url, data,  format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
