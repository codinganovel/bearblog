from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse

from blogs.models import Blog, Post


def analytics(request):
    """Simple analytics view showing basic post statistics"""
    blog = Blog.objects.first()
    if not blog:
        return render(request, '404.html', status=404)

    # Get published posts with basic stats
    posts = Post.objects.filter(publish=True, published_date__lte=timezone.now()).order_by('-published_date')

    # Calculate basic statistics
    total_posts = posts.count()
    published_posts = posts.filter(publish=True).count()
    total_pages = posts.filter(is_page=True).count()

    # Recent posts (last 30 days)
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    recent_posts = posts.filter(published_date__gte=thirty_days_ago).count()

    context = {
        'blog': blog,
        'total_posts': total_posts,
        'published_posts': published_posts,
        'total_pages': total_pages,
        'recent_posts': recent_posts,
        'posts': posts[:10],  # Show 10 most recent posts
    }

    return render(request, 'dashboard/analytics.html', context)


def post_hit(request, uid):
    """Simplified hit tracking - just return success for compatibility"""
    return HttpResponse("Logged")