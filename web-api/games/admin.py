from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import PlayerCreationForm
from .models import (
        Game, Player, PlayerMatchPrediction, FixturePlayerPoints,
)

        
class GameInline(admin.StackedInline):
    model = Game

class FixturePlayerPointsAdmin(admin.ModelAdmin):
    model = FixturePlayerPoints

class PlayerAdmin(admin.ModelAdmin):
    inlines = (GameInline,)
    model = Player
    form = PlayerCreationForm


admin.site.register(Game)
admin.site.register(PlayerMatchPrediction)
admin.site.register(FixturePlayerPoints, FixturePlayerPointsAdmin)
admin.site.register(Player, PlayerAdmin)
