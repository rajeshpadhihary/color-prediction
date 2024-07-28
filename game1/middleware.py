from django.utils import timezone
from datetime import timedelta
from .models import GameRound

class GameRoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # This method is called on each request before the view (and later middleware) are called.
        
        # Clean up old game rounds every time the view is accessed
        one_hour_ago = timezone.now() - timedelta(hours=1)
        GameRound.objects.filter(end_time__lt=one_hour_ago).delete()

        response = self.get_response(request)

        return response
