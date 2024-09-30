import os
import django
import random
from datetime import datetime

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "last_man_standing.settings")  # Replace with your project settings module
django.setup()

from league.models import Team, Gameweek, Player, PlayerSelection

# Teams data
teams = [
    "Bournemouth", "Arsenal", "Aston Villa", "Brentford", "Brighton", "Chelsea",
    "Crystal Palace", "Everton", "Fulham", "Ipswich", "Leicester", "Liverpool",
    "Man City", "Man Utd", "Newcastle", "Forest", "Southampton", "Spurs", "West Ham", "Wolves"
]

# Deadlines for each gameweek
deadlines = [
    "16.08.24 18:15", "24.08.24 11:00", "31.08.24 11:00", "14.09.24 11:00", "21.09.24 11:00", 
    "28.09.24 11:00", "05.10.24 11:00", "19.10.24 11:00", "25.10.24 18:30", "02.11.24 13:30",
    "09.11.24 13:30", "23.11.24 13:30", "30.11.24 13:30", "03.12.24 18:15", "07.12.24 13:30",
    "14.12.24 13:30", "21.12.24 13:30", "26.12.24 13:30", "29.12.24 13:30", "04.01.25 13:30", 
    "14.01.25 18:15", "18.01.25 13:30", "25.01.25 13:30", "01.02.25 13:30", "15.02.25 13:30",
    "22.02.25 13:30", "25.02.25 18:15", "08.03.25 13:30", "15.03.25 13:30", "01.04.25 18:15", 
    "05.04.25 13:30", "12.04.25 13:30", "19.04.25 13:30", "26.04.25 13:30", "03.05.25 13:30",
    "10.05.25 13:30", "18.05.25 13:30", "25.05.25 14:30"
]

# Player names
players = [
    "Craig", "James", "Shug", "Drewzy", "Edan", "Mark", "Ayaan", "Andy", 
    "Chico", "Joe", "Diggity", "Bhatti", "Pat"
]

# Function to convert string to datetime
def parse_deadline(deadline_str):
    # Expected format "DD.MM.YY HH:MM"
    return datetime.strptime(deadline_str, "%d.%m.%y %H:%M")

# Function to populate data
def populate():
    # 1. Create Teams
    team_objects = []
    for team_name in teams:
        team, created = Team.objects.get_or_create(name=team_name)
        team_objects.append(team)
    print(f"Created {len(team_objects)} teams.")

    # 2. Create Gameweeks
    gameweek_objects = []
    for idx, deadline in enumerate(deadlines):
        parsed_deadline = parse_deadline(deadline)  # Correctly parsing the deadline
        gameweek, created = Gameweek.objects.get_or_create(
            number=idx + 1,
            deadline=parsed_deadline
        )
        gameweek_objects.append(gameweek)
    print(f"Created {len(gameweek_objects)} gameweeks.")

    # 3. Create Players
    player_objects = []
    for player_name in players:
        player, created = Player.objects.get_or_create(name=player_name)
        player_objects.append(player)
    print(f"Created {len(player_objects)} players.")


# Call the populate function
if __name__ == '__main__':
    populate()
