from rest_framework.views import APIView
from rest_framework import status
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

from notifications.serializers import NotificationGameSerializer, NotificationFriendSerializer



#https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/authtoken/views.py
class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            token, created = Token.objects.get_or_create(user = user)

            game_notifications = NotificationGameSerializer(user.game_notifications.filter(active = True), many = True)
            friend_notifications = NotificationFriendSerializer(user.friend_notifications.filter(active = True), many = True)

            return Response({'token': token.key, 
                             'username': user.username, 
                             'game_notifications': game_notifications.data,
                             'friend_notifications': friend_notifications.data,
                             'user_id': user.id })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

obtain_auth_token = ObtainAuthToken.as_view()
