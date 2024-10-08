import os
import django
from datetime import datetime

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "last_man_standing.settings")  
django.setup()

from league.models import Team, Gameweek, Player

# Teams data
teams = [
    "Bournemouth", "Arsenal", "Aston Villa", "Brentford", "Brighton", "Chelsea",
    "Crystal Palace", "Everton", "Fulham", "Ipswich", "Leicester", "Liverpool",
    "Man City", "Man Utd", "Newcastle", "Forest", "Southampton", "Spurs", "West Ham", "Wolves", "N/A"
]

# Deadlines for each gameweek
deadlines = [
    "16.08.24 17:15", "24.08.24 10:00", "31.08.24 10:00", "14.09.24 10:00", "21.09.24 10:00",
    "28.09.24 10:00", "05.10.24 10:00", "19.10.24 10:00", "25.10.24 17:30", "02.11.24 12:30",
    "09.11.24 12:30", "23.11.24 12:30", "30.11.24 12:30", "03.12.24 17:15", "07.12.24 12:30",
    "14.12.24 12:30", "21.12.24 12:30", "26.12.24 12:30", "29.12.24 12:30", "04.01.25 12:30",
    "14.01.25 17:15", "18.01.25 12:30", "25.01.25 12:30", "01.02.25 12:30", "15.02.25 12:30",
    "22.02.25 12:30", "25.02.25 17:15", "08.03.25 12:30", "15.03.25 12:30", "01.04.25 17:15",
    "05.04.25 12:30", "12.04.25 12:30", "19.04.25 12:30", "26.04.25 12:30", "03.05.25 12:30",
    "10.05.25 12:30", "18.05.25 12:30", "25.05.25 13:30"
]

# Results-in times for each gameweek (same format as deadlines)
matchweek_times = [
    "19.08.24 23:00", "25.08.24 19:30", "01.09.24 19:00", "15.09.24 19:30", "22.09.24 19:30",
    "30.09.24 23:00", "06.10.24 19:30", "21.10.24 23:00", "27.10.24 19:30", "04.11.24 23:00",
    "10.11.24 19:30", "25.11.24 23:00", "01.12.24 19:00", "04.12.24 23:00", "07.12.24 20:30",
    "14.12.24 23:00", "21.12.24 20:30", "26.12.24 23:00", "29.12.24 19:00", "04.01.25 20:30",
    "15.01.25 23:00", "18.01.25 20:30", "25.01.25 20:30", "01.02.25 20:30", "15.02.25 20:30",
    "22.02.25 20:30", "26.02.25 23:00", "08.03.25 20:30", "15.03.25 20:30", "02.04.25 23:00",
    "05.04.25 20:30", "12.04.25 20:30", "19.04.25 20:30", "26.04.25 20:30", "03.05.25 20:30",
    "10.05.25 20:30", "18.05.25 19:00", "25.05.25 19:00"
]

# Player names
players = [
    "Craig", "James", "Shug", "Drewzy", "Edan", "Mark", "Ayaan", "Andy", 
    "Chico", "Joe", "Diggity", "Bhatti", "Pat"
]

# Function to convert string to datetime
def parse_datetime(datetime_str):
    # Expected format "DD.MM.YY HH:MM"
    return datetime.strptime(datetime_str, "%d.%m.%y %H:%M")

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
    for idx, (deadline, results_in) in enumerate(zip(deadlines, matchweek_times)):
        parsed_deadline = parse_datetime(deadline)
        parsed_results_in = parse_datetime(results_in)
        gameweek, created = Gameweek.objects.get_or_create(
            number=idx + 1,
            deadline=parsed_deadline,
            results_in=parsed_results_in
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
