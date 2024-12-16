from django.shortcuts import render, redirect
from .models import Player
from django.http import HttpResponse
import random

def home_page(request):
   
    players = Player.objects.all().order_by('-votes', 'name')
    
    
    def build_tree(players):
        tree = []
        level_size = 1
        index = 0

        while index < len(players):
            level = players[index:index + level_size]
            tree.append(level)
            index += level_size
            level_size *= 2  

        return tree

    players_tree = build_tree(list(players))
    return render(request, 'home_page.html', {'players_tree': players_tree})

def voting_page(request):
    if 'current_player' not in request.session:
        request.session['current_player'] = None

    if 'remaining_players' not in request.session:
        request.session['remaining_players'] = list(Player.objects.values_list('id', flat=True))
        random.shuffle(request.session['remaining_players'])

  
    if not request.session['remaining_players']:
        request.session['current_player'] = None
        return redirect('home_page')

 
    if request.session['current_player'] is None:
        request.session['current_player'] = request.session['remaining_players'].pop()

    current_player = Player.objects.get(id=request.session['current_player'])
    challenger_id = request.session['remaining_players'].pop()
    challenger = Player.objects.get(id=challenger_id)

    request.session['challenger'] = challenger.id
    request.session.modified = True

    return render(request, 'voting_page.html', {
        'current_player': current_player,
        'challenger': challenger,
    })

def vote_player(request, winner_id, loser_id):
    winner = Player.objects.get(id=winner_id)
    loser = Player.objects.get(id=loser_id)

    
    winner.votes += 1
    winner.save()

   
    request.session['current_player'] = winner.id

    return redirect('voting_page')