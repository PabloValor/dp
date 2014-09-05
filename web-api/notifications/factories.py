import factory
from .models import NotificationGame, NotificationFriend
from games.factories import PlayerFactory, GameFactory

class NotificationGameFactory(factory.Factory):
    player = factory.LazyAttribute(lambda a: PlayerFactory())
    sender = factory.LazyAttribute(lambda a: PlayerFactory())
    game = factory.LazyAttribute(lambda a: GameFactory())
    active = True
    notification_type = '1'

class NotificationFriendFactory(factory.Factory):
    player = factory.LazyAttribute(lambda a: PlayerFactory())
    sender = factory.LazyAttribute(lambda a: PlayerFactory())
    active = True
    notification_type = '1'
