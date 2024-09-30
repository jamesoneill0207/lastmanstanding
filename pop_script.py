import os
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'last_man_standing.settings')

import django
django.setup()


from league.models import Team, Gameweek, Player, PlayerSelection, TeamResult
import random
from django.utils import timezone

# Your population script
def populate():
    # Clear existing data
    PlayerSelection.objects.all().delete()
    TeamResult.objects.all().delete()
    Gameweek.objects.all().delete()
    Player.objects.all().delete()
    Team.objects.all().delete()

    # Create Teams
    team_names = [
        'Team A', 'Team B', 'Team C', 'Team D', 'Team E',
        'Team F', 'Team G', 'Team H', 'Team I', 'Team J',
        'Team K', 'Team L', 'Team M', 'Team N', 'Team O',
        'Team P', 'Team Q', 'Team R', 'Team S', 'Team T'
    ]

    teams = []
    for name in team_names:
        team = Team.objects.create(name=name)
        teams.append(team)
    
    print(f'Created {len(teams)} teams.')

    # Create Gameweeks
    gameweeks = []
    for i in range(1, 39):  # 38 Gameweeks
        gameweek = Gameweek.objects.create(
            number=i,
            deadline=timezone.now() + timezone.timedelta(days=i * 7)
        )
        gameweeks.append(gameweek)
    
    print(f'Created {len(gameweeks)} gameweeks.')

    # Create Players
    player_names = ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5']
    players = []
    for name in player_names:
        player = Player.objects.create(name=name, is_standing=True)
        players.append(player)

    print(f'Created {len(players)} players.')

    # Assign Team Results
    for gameweek in gameweeks:
        for team in teams:
            result = random.choice(['W', 'L', 'NP'])
            TeamResult.objects.create(team=team, gameweek=gameweek, result=result)

    print('Assigned random results to teams for each gameweek.')

    # Make Player Selections
    for player in players:
        for gameweek in gameweeks:
            team = random.choice(teams)
            PlayerSelection.objects.create(player=player, gameweek=gameweek, team=team)
    
    print('Assigned random team selections for each player in every gameweek.')
    print('Database population complete!')

if __name__ == '__main__':
    populate()