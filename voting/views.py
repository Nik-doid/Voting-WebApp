from django.shortcuts import render, redirect
from .models import Player
from django.http import HttpResponse
import random
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


def calculate_elo(winner_rating, loser_rating, k=32):
    """
    Update the Elo ratings for a winner and loser.
    """
    # Calculate expected scores
    expected_winner = 1 / (1 + 10 ** ((loser_rating - winner_rating) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner_rating - loser_rating) / 400))
    
    # Update ratings
    new_winner_rating = winner_rating + k * (1 - expected_winner)
    new_loser_rating = loser_rating + k * (0 - expected_loser)
    
    return round(new_winner_rating, 2), round(new_loser_rating, 2)


def home_page(request):
    players = Player.objects.all().order_by('-votes', 'name')
    
    # Print player ratings for debugging
    for player in players:
        print(f"Player: {player.name}, Rating: {player.rating}")  # Reading the rating, not setting it
    
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
    # Initialize session variables if not set
    if 'current_player' not in request.session:
        request.session['current_player'] = None

    if 'remaining_players' not in request.session:
        # Create a shuffled list of player IDs for voting
        request.session['remaining_players'] = list(Player.objects.values_list('id', flat=True))
        random.shuffle(request.session['remaining_players'])

    # Check if all players are exhausted
    if not request.session['remaining_players']:
        request.session['current_player'] = None
        return redirect('home_page')

    # Set the current player if not already set
    if request.session['current_player'] is None:
        request.session['current_player'] = request.session['remaining_players'].pop()

    # Get the current player and challenger from the database
    current_player = Player.objects.get(id=request.session['current_player'])
    challenger_id = request.session['remaining_players'].pop()
    challenger = Player.objects.get(id=challenger_id)

    # Save the challenger in the session for the voting process
    request.session['challenger'] = challenger.id
    request.session.modified = True

    return render(request, 'voting_page.html', {
        'current_player': current_player,
        'challenger': challenger,
    })


def vote_player(request, winner_id, loser_id):
    winner = Player.objects.get(id=winner_id)
    loser = Player.objects.get(id=loser_id)

    # Update Elo ratings
    winner.rating, loser.rating = calculate_elo(winner.rating, loser.rating)
    
    # Increment the winner's vote count
    winner.votes += 1

    # Save updated data to the database
    winner.save()
    loser.save()

    # Set the winner as the next 'current_player' for the session
    request.session['current_player'] = winner.id

    return redirect('voting_page')

