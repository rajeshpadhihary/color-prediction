from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import GameRound, UserPrediction
import random
from datetime import timedelta

@login_required
def game_view(request):
    # Clean up old game rounds
    one_hour_ago = timezone.now() - timedelta(hours=1)
    GameRound.objects.filter(end_time__lt=one_hour_ago).delete()

    # Get the current game round or create a new one if none exists
    now = timezone.now()
    game_round = GameRound.objects.filter(end_time__gte=now).first()

    if not game_round:
        correct_color = random.choice(['red', 'green', 'blue', 'yellow'])
        game_round = GameRound.objects.create(
            round_number=GameRound.objects.count() + 1,
            correct_color=correct_color,
            end_time=now + timedelta(minutes=2)
        )

    existing_prediction = UserPrediction.objects.filter(user=request.user, game_round=game_round).first()

    if request.method == 'POST' and not existing_prediction:
        color = request.POST.get('color')
        is_correct = color == game_round.correct_color
        UserPrediction.objects.create(
            user=request.user,
            game_round=game_round,
            predicted_color=color,
            is_correct=is_correct
        )

    # Get the last 10 predictions for the user
    last_10_predictions = UserPrediction.objects.filter(user=request.user).order_by('-game_round__round_number')[:10]

    context = {
        'game_round': game_round,
        'existing_prediction': existing_prediction,
        'last_10_predictions': last_10_predictions,
        'now': timezone.now(),
    }
    return render(request, 'game.html', context)

@login_required
def result_view(request):
    now = timezone.now()
    last_game_round = GameRound.objects.filter(end_time__lte=now).order_by('-round_number').first()
    prediction = UserPrediction.objects.filter(user=request.user, game_round=last_game_round).first()

    context = {
        'last_game_round': last_game_round,
        'prediction': prediction,
    }
    return render(request, 'result.html', context)

@login_required
def game_page(request):
    return render(request, 'game_page.html')
