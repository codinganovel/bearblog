from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.utils.text import slugify

from blogs.models import Blog, Post
from blogs.helpers import unmark

def get_blog():
    """Get the single blog instance for personal CMS"""
    blog = Blog.objects.first()
    if not blog:
        # Create default blog if none exists
        blog = Blog.objects.create(
            title="My Personal Blog",
            content="Welcome to my personal blog!"
        )
    return blog


def home(request):
    blog = get_blog()

    all_posts = Post.objects.filter(publish=True, published_date__lte=timezone.now(), is_page=False).order_by('-published_date')

    meta_description = blog.meta_description or unmark(blog.content)[:157] + '...'

    return render(
        request,
        'home.html',
        {
            'blog': blog,
            'posts': all_posts,
            'meta_description': meta_description
        }
    )


def posts(request):
    blog = get_blog()

    tag_param = request.GET.get('q', '')
    tags = [t.strip() for t in tag_param.split(',')] if tag_param else []
    tags = [t for t in tags if t]  # Remove empty strings

    posts = Post.objects.filter(publish=True, published_date__lte=timezone.now(), is_page=False).order_by('-published_date')
    if tags:
        # Filter posts that contain ALL specified tags
        posts = [post for post in posts if all(tag in post.tags for tag in tags)]
        
        available_tags = set()
        for post in posts:
            available_tags.update(post.tags)

    else:
        available_tags = set(blog.tags)

    meta_description = blog.meta_description or unmark(blog.content)[:157] + '...'

    blog_path_title = 'Blog'

    return render(
        request,
        'posts.html',
        {
            'blog': blog,
            'posts': posts,
            'meta_description': meta_description,
            'query': tag_param,
            'active_tags': tags,
            'available_tags': available_tags,
            'blog_path_title': blog_path_title
        }
    )


def post(request, slug):
    # Prevent null characters in path
    slug = slug.replace('\x00', '')

    if slug[0] == '/' and slug[-1] == '/':
        slug = slug[1:-1]

    blog = get_blog()

    # Check for RSS feed path
    if slug == blog.rss_alias:
        from blogs.views.feed import feed
        return feed(request)

    # Find by post slug
    post = Post.objects.filter(slug__iexact=slug).first()

    if not post:
        # Find by post alias
        post = Post.objects.filter(alias__iexact=slug).first()

        if post:
            return redirect('post', slug=post.slug)
        else:
            # Check for blog path and render the blog page
            if slug == 'blog':
                return posts(request)

            return render(request, '404.html', {'blog': blog}, status=404)

    meta_description = post.meta_description or unmark(post.content)[:157] + '...'
    canonical_url = post.canonical_url if post.canonical_url and post.canonical_url.startswith('https://') else f'/{post.slug}/'

    if post.publish is False and not request.GET.get('token') == post.token:
        return not_found(request)

    context = {
        'blog': blog,
        'post': post,
        'canonical_url': canonical_url,
        'meta_description': meta_description,
        'meta_image': post.meta_image or blog.meta_image,
    }

    return render(request, 'post.html', context)


def not_found(request, *args, **kwargs):
    blog = get_blog()
    return render(request, '404.html', {'blog': blog}, status=404)


def sitemap(request):
    blog = get_blog()

    try:
        posts = Post.objects.filter(publish=True, published_date__lte=timezone.now()).only('slug', 'last_modified').order_by('-published_date')
    except AttributeError:
        posts = []

    return render(request, 'sitemap.xml', {'blog': blog, 'posts': posts}, content_type='text/xml')


def robots(request):
    blog = get_blog()

    return render(request, 'robots.txt',  {'blog': blog}, content_type="text/plain")
