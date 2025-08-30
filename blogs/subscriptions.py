from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def lemon_webhook(request):
    """Simplified webhook handler - subscription management removed for personal CMS"""
    return HttpResponse("OK")


def get_subscriptions(order_id=None, user_email=None):
    """Simplified subscription function - returns None for personal CMS"""
    # For personal CMS, no subscription management needed
    return None