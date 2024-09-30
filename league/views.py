from django.shortcuts import render
from django.http import HttpResponse
from league.models import Gameweek, PlayerSelection, Player, Team, TeamResult, update_player_selection_result
from league.forms import predictionForm
from django.utils import timezone


# Helper function to handle the team picking logic
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


def process_predictions_and_context(players, gameweeks, teams, context):
    predictions = []
    all_teams = []
    all_players = []
    no_still_standing = 0
    most_recent_gw = 0

    for team in teams:
        all_teams.append(team)
    
    for player in players:
        picks = []
        all_players.append(player)
        picks.append(player)
        for gw in gameweeks:
            try:
                selection = PlayerSelection.objects.get(player=player, gameweek=gw)
                if gw.number > most_recent_gw:
                    most_recent_gw = gw.number

                if selection.team.name == "N/A":  
                    picks.append(selection.team.name)
                else:
                    picks.append(selection.team.name + " - " + selection.result)
                
                if selection.result == 'L' and player.is_standing:
                    player.is_standing = False
                    player.week_lost = gw.number
            except PlayerSelection.DoesNotExist:
                if player.is_standing and gw.deadline < timezone.now():
                    player.is_standing = False
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
                
    elif no_still_standing == 0:
        for player in players:
            if player.week_lost == most_recent_gw:
                player.is_standing = True
                player.week_lost = 0

    context["predictions"] = predictions
    context['all_teams'] = all_teams
    context['players'] = all_players
    context['gameweeks_range'] = range(gameweeks.count())
    context['gameweeks'] = gameweeks

def gw1_19(request):

    
    players = Player.objects.all()
    gameweeks = Gameweek.objects.filter(number__lte=19)  
    teams = Team.objects.all()
    form = predictionForm()
    context = {'form': form, "winner": False}
    all_results = TeamResult.objects.all()

    for result in all_results:
        update_player_selection_result(sender=TeamResult, instance=result)

    if request.method == 'POST':
        handle_team_pick(request, context)

    process_predictions_and_context(players, gameweeks, teams, context)

    return render(request, 'league/gw1-19.html', context)


# View for Gameweeks 20-38
def gw20_38(request):
    players = Player.objects.all()
    gameweeks = Gameweek.objects.filter(number__gte=20)
    teams = Team.objects.all()
    form = predictionForm()
    context = {'form': form, "winner": False}
    all_results = TeamResult.objects.all()

    for result in all_results:
        update_player_selection_result(sender=TeamResult, instance=result)

    if request.method == 'POST':
        handle_team_pick(request, context)

    process_predictions_and_context(players, gameweeks, teams, context)

    return render(request, 'league/gw20-38.html', context)
