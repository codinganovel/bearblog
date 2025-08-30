from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from blogs.models import Blog
from blogs.views.blog import get_blog


def email_list(request):
    """Simplified email list - no subscribers in personal CMS"""
    blog = get_blog()
    # For personal CMS, just show a message that email subscriptions are not available
    return render(request, 'dashboard/email_list.html', {
        'blog': blog,
        'message': 'Email subscription management is not available in this personal CMS version.'
    })


def subscribe(request):
    """Simplified subscribe - not available in personal CMS"""
    blog = get_blog()
    return render(request, 'subscribe.html', {'blog': blog})


@csrf_exempt
def email_subscribe(request):
    """Simplified email subscribe - not available in personal CMS"""
    return HttpResponse("Email subscriptions are not available in this personal CMS version.")


def confirm_subscription(request):
    """Simplified confirm subscription - not available in personal CMS"""
    return HttpResponse("Email subscriptions are not available in this personal CMS version.")