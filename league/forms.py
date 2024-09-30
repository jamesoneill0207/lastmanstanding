from django import forms
from league.models import PlayerSelection

class predictionForm(forms.ModelForm):
    class Meta:
        model = PlayerSelection
        fields = ['player', 'team', 'gameweek']
