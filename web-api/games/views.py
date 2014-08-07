from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Game, Player, GamePlayer, PlayerFriend
from .serializers import ( GameSerializer, PlayerSerializer, PlayerCreateSerializer, PlayerUpdateSerializer, 
                           PlayerSearchSerializer, PlayerFriendSerializer, GamePlayerUpdateSerializer)

from .permissions import IsOwnerOrReadOnly, IsSameUser, IsFriend

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
        return user.games.all()


class GameCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user

    def post_save(self, obj, created=False):
        if not obj.players.filter(id = obj.owner.id).exists():
            game_player = GamePlayer.objects.create(player = obj.owner, game = obj, status = True)
            game_player.save()

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user

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

    def pre_save(self, obj):
        obj.player = self.request.user

        # If the player who rejected the last invitation creates a new one
        # we delete the old one (maybe in the future we will like to save this info)
        PlayerFriend.objects.filter(friend =  obj.player, player = obj.friend, status = False).delete()

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
          


from social.apps.django_app.utils import strategy

@strategy()
@api_view(['POST'])
def social_register(request, backend):
    auth_token = request.DATA.get('access_token', None)
    if auth_token:
        try:
            user = request.strategy.backend.do_auth(access_token=auth_token)
        except Exception, err:
            return Response(str(err), status=400)

        if user:
          return Response({ 'token': user.auth_token.key, 'username': user.username },  status=status.HTTP_200_OK )
        else:
            return Response("Bad Credentials", status=403)
    else:
        return Response("Bad request", status=400)

