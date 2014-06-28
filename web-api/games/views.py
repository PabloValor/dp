from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Game, Player
from .serializers import GameSerializer, PlayerSerializer, PlayerCreateSerializer, PlayerUpdateSerializer
from .permissions import IsOwnerOrReadOnly, IsSameUser

class GameList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user.player

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user.player

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

from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from social.apps.django_app.utils import strategy, load_strategy 
from social.apps.django_app.views import _do_login

@strategy()
def auth_by_token(request, backend):
    backend = request.strategy.backend
    user=request.user
    user = backend.do_auth(
        access_token=request.DATA.get('access_token'),
        user=user.is_authenticated() and user or None
        )

    import ipdb; ipdb.set_trace()
    if user and user.is_active:
        return user
    else:
        return None
        
@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def social_register(request):
    auth_token = request.DATA.get('access_token', None)
    backend = request.DATA.get('backend', None)
    if auth_token and backend:
        try:
            user = auth_by_token(request, backend)
        except Exception, err:
            return Response(str(err), status=400)
        if user:
            strategy = load_strategy(request=request, backend=backend)
            import ipdb; ipdb.set_trace()
            _do_login(strategy, user, user.social_user)
            return Response( "User logged in", status=status.HTTP_200_OK )
        else:
            return Response("Bad Credentials", status=403)
    else:
        return Response("Bad request", status=400)
