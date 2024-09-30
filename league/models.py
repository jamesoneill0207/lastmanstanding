from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class LastManStanding(models.Model):
    winner = models.BooleanField(default=False)

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Gameweek(models.Model):
    number = models.PositiveIntegerField(unique=True)
    deadline = models.DateTimeField()
    
    def __str__(self):
        return f"Gameweek {self.number}"
    
class Player(models.Model):
    name = models.CharField(max_length=100)
    is_standing = models.BooleanField(default=True)
    winner = models.BooleanField(default=False)
    week_lost = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class PlayerSelection(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=False, blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, blank=False)
    gameweek = models.ForeignKey(Gameweek, on_delete=models.CASCADE, null=False, blank=False)
    result = models.CharField(max_length=1, default='?')

    def __str__(self):
        return f"{self.player.name} picked {self.team.name} in GW {self.gameweek.number}"
    
class TeamResult(models.Model):
    result = models.CharField(max_length=1, default='?')  
    gameweek = models.ForeignKey(Gameweek, on_delete=models.CASCADE, null=False, blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"Result for {self.team.name} in GW {self.gameweek.number}: {self.result}"

def update_player_selection_result(sender, instance, **kwargs):
    player_selections = PlayerSelection.objects.filter(team=instance.team, gameweek=instance.gameweek)
    
    for selection in player_selections:
        selection.result = instance.result
        selection.save()

