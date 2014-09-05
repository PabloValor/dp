from django.http import Http404
from rest_framework import  permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import NotificationGame, NotificationFriend

@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def notification_update(request, pk, notification_type):
    try:
      user = request.user

      if notification_type == 'game':
          notification = NotificationGame.objects.get(pk = pk, player = user)
      elif notification_type == 'friend':
          notification = NotificationFriend.objects.get(pk = pk, player = user)
      else:
          raise Http404

      notification.active = False
      notification.save()

      return Response(status = status.HTTP_202_ACCEPTED)

    except (NotificationGame.DoesNotExist, NotificationFriend.DoesNotExist):
      return Response(status = status.HTTP_404_NOT_FOUND)
