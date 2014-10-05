from django.shortcuts import render
from rest_framework import generics, permissions, status
from .serializers import ContactSerializer

class ContactCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ContactSerializer

    def pre_save(self, obj):
        obj.player = self.request.user
