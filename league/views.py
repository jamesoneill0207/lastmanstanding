from django.shortcuts import render
from django.http import HttpResponse
from league.models import Gameweek, PlayerSelection, Player, Team, TeamResult, update_player_selection_result
from league.forms import predictionForm
from django.utils import timezone
import requests
import json
from django.conf import settings

def add_results(week):

    current_week = str(week.number)
   
    team_names = {
    "Newcastle United FC": "Newcastle",
    "Manchester City FC": "Man City",
    "Arsenal FC": "Arsenal",
    "Leicester City FC": "Leicester",
    "Brentford FC": "Brentford",
    "West Ham United FC": "West Ham",
    "Chelsea FC": "Chelsea",
    "Brighton & Hove Albion FC": "Brighton",
    "Everton FC": "Everton",
    "Crystal Palace FC": "Crystal Palace",
    "Fulham FC": "Fulham",
    "Nottingham Forest FC": "Forest",
    "Liverpool FC": "Liverpool",
    "Wolverhampton Wanderers FC": "Wolves",
    "Ipswich Town FC": "Ipswich",
    "Aston Villa FC": "Aston Villa",
    "Tottenham Hotspur FC": "Spurs",
    "Manchester United FC": "Man Utd",
    "AFC Bournemouth": "Bournemouth",
    "Southampton FC": "Southampton"}

    API_KEY = settings.API_KEY
    uri = f'https://api.football-data.org/v4/competitions/PL/matches?matchday={current_week}'
    headers = { 'X-Auth-Token': API_KEY }

    response = requests.get(uri, headers=headers)

    for match in response.json()['matches']:
       
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        try:
            winner = match['score']['winner']
        except:
            break
        home_team_obj = Team.objects.get(name=team_names.get(home_team))
        away_team_obj = Team.objects.get(name=team_names.get(away_team))

        if winner == 'HOME_TEAM':
           TeamResult.objects.get_or_create(
                        result="W", gameweek=week, team=home_team_obj)
           TeamResult.objects.get_or_create(
                        result="L", gameweek=week, team=away_team_obj)
        elif winner == 'AWAY_TEAM':
            TeamResult.objects.get_or_create(
                        result="W", gameweek=week, team=away_team_obj)
            TeamResult.objects.get_or_create(
                        result="L", gameweek=week, team=home_team_obj)
        elif winner == 'DRAW':
            TeamResult.objects.get_or_create(
                        result="L", gameweek=week, team=home_team_obj)
            TeamResult.objects.get_or_create(
                        result="L", gameweek=week, team=away_team_obj)

def handle_team_pick(request, context):
    picked_team = request.POST.get('team')
    player_pick = request.POST.get('player')
    gw_pick = request.POST.get('gameweek')
    
    if picked_team and player_pick and gw_pick:
        try:
            team = Team.objects.get(name=picked_team)
            player_name = Player.objects.get(name=player_pick)
            gameweek = Gameweek.objects.get(number=gw_pick)
            
            gw_of_other = PlayerSelection.objects.filter(player=player_name, team=team)

            if gw_of_other.count() == 2:
                context['error'] = "You have already selected this team twice"
            elif gw_of_other.count() == 1:
                other_selection = gw_of_other.first()
                if int(gw_pick) < 21 and other_selection.gameweek.number < 21:
                    context['error'] = 'You cannot pick this team twice before gameweek 21'
                elif int(gw_pick) > 20 and other_selection.gameweek.number > 20:
                    context['error'] = "You cannot pick this team twice after gameweek 20"
                else:
                    PlayerSelection.objects.filter(player=player_name, gameweek=gameweek).delete()
                    PlayerSelection.objects.get_or_create(
                        player=player_name, gameweek=gameweek, team=team)
            else:
                PlayerSelection.objects.filter(player=player_name, gameweek=gameweek).delete()
                PlayerSelection.objects.get_or_create(
                    player=player_name, gameweek=gameweek, team=team)
        except (Team.DoesNotExist, Player.DoesNotExist, Gameweek.DoesNotExist) as e:
            print(f"Error: {e}")

def process_predictions_and_context(players, gameweeks, context):
    predictions = []
    all_teams = []
    all_players = []
    no_still_standing = 0
    most_recent_gw = Gameweek.objects.get(number = 1)
    selectable_gw = []
    teams = Team.objects.all()

    for team in teams:
        all_teams.append(team)
    
    for player in players:
        picks = []
        all_players.append(player)
        picks.append(player)
        for gw in gameweeks:
            try:
                
                selection = PlayerSelection.objects.get(player=player, gameweek=gw)
                if gw.deadline > most_recent_gw.deadline and gw.deadline < timezone.now():
                    most_recent_gw = gw
                    
                if selection.team.name == "N/A":  
                    picks.append(selection.team.name)
                else:
                    picks.append(selection.team.name + " - " + selection.result)
                
                if selection.result == 'L' and player.is_standing and gw.weeks_to_ignore == False:
                    player.is_standing = False
                    player.week_lost = gw.number
            except (PlayerSelection.DoesNotExist):
                if player.is_standing and gw.deadline < timezone.now():
                    player.is_standing = False
                    player.week_lost = gw.number
                    PlayerSelection.objects.get_or_create(
                        player=player, gameweek=gw, team = Team.objects.get(name="N/A"))
                    
                picks.append("")
        player.save()

        if player.is_standing:
            no_still_standing += 1
            
        predictions.append(picks)

    if no_still_standing == 1:
        for player in players:
            if player.is_standing:
                player.winner = True
                context["winner"] = True
            player.save()
                
    elif no_still_standing == 0:
        for player in players:
            if player.week_lost == most_recent_gw.number:
                player.is_standing = True
                player.week_lost = 0
                most_recent_gw.weeks_to_ignore = True            
            player.save()
        most_recent_gw.save()

    context['gameweeks_range'] = gameweeks

    for gw in gameweeks:
        if gw.deadline > timezone.now():
            selectable_gw.append(gw)

    context["predictions"] = predictions
    context['all_teams'] = all_teams
    context['players'] = all_players
    context['gameweeks'] = selectable_gw

def gw1_19(request):

    players = Player.objects.all()
    gameweeks = Gameweek.objects.filter(number__lte=19)  
   
    form = predictionForm()
    context = {'form': form, "winner": False}
    all_results = TeamResult.objects.all()
    
    for gw in gameweeks:
        if gw.results_in < timezone.now() and gw.all_results == False:
            add_results(gw)
            gw.all_results = True
            gw.save()

    for result in all_results:
        update_player_selection_result(sender=TeamResult, instance=result)

    if request.method == 'POST':
        handle_team_pick(request, context)

    process_predictions_and_context(players, gameweeks, context)

    return render(request, 'league/gw1-19.html', context)

def gw20_38(request):

    
    players = Player.objects.all()
    gameweeks = Gameweek.objects.filter(number__gte=20)
    form = predictionForm()
    context = {'form': form, "winner": False}
    all_results = TeamResult.objects.all()

    for gw in gameweeks:
        if gw.results_in < timezone.now() and gw.all_results == False:
            add_results(gw)
            gw.all_results = True
            gw.save()

    for result in all_results:
        update_player_selection_result(sender=TeamResult, instance=result)

    if request.method == 'POST':
        handle_team_pick(request, context)

    process_predictions_and_context(players, gameweeks, context)

    return render(request, 'league/gw20-38.html', context)
