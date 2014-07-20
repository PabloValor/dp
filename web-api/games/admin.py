from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import PlayerCreationForm
from .models import (
        Game, Player, PlayerMatchPrediction, FixturePlayerPoints, GamePlayer
)


class GamePlayerInline(admin.StackedInline):
    model = GamePlayer

class GameAdmin(admin.ModelAdmin):
    inlines = (GamePlayerInline,)

class GameInline(admin.StackedInline):
    model = Game

class PlayerAdmin(admin.ModelAdmin):
    inlines = (GameInline,)


admin.site.register(Game, GameAdmin)
admin.site.register(PlayerMatchPrediction)
admin.site.register(FixturePlayerPoints)
admin.site.register(Player, PlayerAdmin)
