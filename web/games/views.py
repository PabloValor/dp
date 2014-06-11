from rest_framework import generics, permissions
from .models import Game, Player
from .serializers import GameSerializer, PlayerSerializer
from .permissions import IsOwnerOrReadOnly

class GameList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user.player

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user.player

class PlayerList(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetail(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

