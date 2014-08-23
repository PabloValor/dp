from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import (
        Game, Player, PlayerMatchPrediction, FixturePlayerPoints, GamePlayer, PlayerFriend
)


class GamePlayerInline(admin.StackedInline):
    model = GamePlayer

class GameAdmin(admin.ModelAdmin):
    inlines = (GamePlayerInline,)

class GameInline(admin.StackedInline):
    model = Game

class PlayerAdmin(admin.ModelAdmin):
    inlines = (GameInline,)

class PlayerMatchPredictionAdmin(admin.ModelAdmin):
    inlines = (GameInline,)
    list_display = ['game', 'match', 'local_team_goals', 'visitor_team_goals']
    list_display_links = ['game']

admin.site.register(Game, GameAdmin)
admin.site.register(PlayerMatchPrediction, PlayerMatchPredictionAdmin)
admin.site.register(FixturePlayerPoints)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerFriend)
