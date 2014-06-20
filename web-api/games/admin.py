from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import PlayerCreationForm
from .models import (
        Game, Player, PlayerMatchPrediction, FixturePlayerPoints,
)

class PlayerInline(admin.StackedInline):
    model = Player
        
class GameAdmin(admin.ModelAdmin):
    inlines = (PlayerInline,)

class FixturePlayerPointsAdmin(admin.ModelAdmin):
    model = FixturePlayerPoints

class PlayerAdmin(admin.ModelAdmin):
    model = Player
    form = PlayerCreationForm


admin.site.register(Game, GameAdmin)
admin.site.register(PlayerMatchPrediction)
admin.site.register(FixturePlayerPoints, FixturePlayerPointsAdmin)
admin.site.register(Player, PlayerAdmin)
