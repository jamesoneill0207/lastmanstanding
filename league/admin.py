from django.contrib import admin
from league.models import Team, PlayerSelection, Gameweek, Player, TeamResult

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Gameweek)
admin.site.register(PlayerSelection)
admin.site.register(TeamResult)

