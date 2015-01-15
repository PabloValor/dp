from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Game, Player, GamePlayer, PlayerFriend, PlayerMatchPrediction
from .serializers import ( GameSerializer, PlayerSerializer, PlayerCreateSerializer, PlayerUpdateSerializer, 
                           PlayerSearchSerializer, PlayerFriendSerializer, GamePlayerUpdateSerializer,
                           GamePlayerCreateSerializer, GamePlayerUpdateAnotherChanceSerializer, GamePlayerUpdateInvitesAgainSerializer,
                           PlayerMatchPredictionSerializer, PlayerMatchPredictionListSerializer,)

from .permissions import *

class GamePlayerUpdateAnotherChance(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GamePlayerUpdateAnotherChanceSerializer

    def get_queryset(self):
        user = self.request.user
        return user.gameplayer_set.filter(status = False, another_chance = None)

class GamePlayerUpdateInvitesAgain(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GamePlayerUpdateInvitesAgainSerializer

    def get_queryset(self):
        user = self.request.user
        return GamePlayer.objects.filter(status = False, another_chance = True, game__owner = user)

    def pre_save(self, obj):
        obj.reset()

class GamePlayerUpdate(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GamePlayerUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        return user.gameplayer_set

class GameList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GameSerializer

    def get_queryset(self):
        user = self.request.user
        games = user.games.all()
        if not games.exists():
            raise Http404

        return games


class GameCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class PlayerMatchPredictionCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, PlayerMatchPredictionPermission)
    serializer_class = PlayerMatchPredictionSerializer

class PlayerMatchPredictionList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, SameGamePlaying, OpenGame)
    serializer_class = PlayerMatchPredictionListSerializer

    def get_queryset(self):
        user = self.request.user
        gameplayer_id = self.kwargs['gp']

        return PlayerMatchPrediction.objects.filter(gameplayer__id = gameplayer_id).order_by('match__fixture__number')

class PlayerList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerCreate(generics.CreateAPIView):
    serializer_class = PlayerCreateSerializer

class PlayerUpdate(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsSameUser,)
    queryset = Player.objects.all()
    serializer_class = PlayerUpdateSerializer

class PlayerListSearch(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlayerSearchSerializer

    def get_queryset(self):
        user = self.request.user
        username = self.kwargs['username'].strip()
        if len(username) == 0:
          return []

        return Player.objects.exclude(id = user.id).filter(username__icontains=username)

class PlayerFriendsList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlayerSearchSerializer

    def get_queryset(self):
        user = self.request.user
        return user.get_all_friends()

class PlayerFriendCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlayerFriendSerializer


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def player_friend_update(request, pk):
    if not request.DATA.has_key('status'):
      return Response(status = status.HTTP_400_BAD_REQUEST)

    try:
      user = request.user
      pf = user.friend.get(player__pk = pk, status = None) 
      pf.status = request.DATA['status']
      pf.save()

      return Response(status = status.HTTP_200_OK)

    except PlayerFriend.DoesNotExist:
      return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def game_player_create(request):
    serializer = GamePlayerCreateSerializer(data=request.data, many = True, context = {'request': request })
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from social.apps.django_app.utils import psa
from notifications.serializers import NotificationGameSerializer, NotificationFriendSerializer
from social.backends.facebook import FacebookAppOAuth2, FacebookOAuth2


@psa()
@api_view(['POST'])
def social_register(request, backend):
    if isinstance(request.backend, FacebookAppOAuth2) or isinstance(request.backend, FacebookOAuth2):
        auth_token = request.DATA.get('access_token', None)
        if auth_token:
            try:
                user = request.backend.do_auth(access_token=auth_token)
            except Exception, err:
                return Response(str(err), status=400)

            if user:
                game_notifications = NotificationGameSerializer(user.game_notifications.filter(active = True), many = True)
                friend_notifications = NotificationFriendSerializer(user.friend_notifications.filter(active = True), many = True)

                return Response({ 'token': user.auth_token.key, 
                                  'username': user.username, 
                                  'game_notifications': game_notifications.data,
                                  'friend_notifications': friend_notifications.data,
                                  'user_id': user.id },  
                                status=status.HTTP_200_OK )
            else:
                return Response("Bad Credentials", status=403)

    return Response("Bad request", status=400)

