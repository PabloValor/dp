from django.contrib import admin
from .models import (
        Match, Team, Fixture, Tournament, 
)

class MatchInline(admin.TabularInline):
    model = Match

class FixtureInline(admin.StackedInline):
    model = Fixture

class FixtureAdmin(admin.ModelAdmin):
    inlines = (MatchInline,)
    list_display = ['tournament', '__unicode__']
    list_display_links = ['__unicode__']
    list_filter = ['tournament']

class TournamentAdmin(admin.ModelAdmin):
    inlines = (FixtureInline,)

class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = ['name', 'crest_thumbnail', 'crest']
    list_editable = ['crest']

admin.site.register(Team, TeamAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(Tournament, TournamentAdmin)
