from django.contrib import admin
from django.db.models import Count
from django.utils.html import escape, format_html
from django.urls import reverse

from blogs.models import Blog, Post, Stylesheet, Media


admin.site.enable_nav_sidebar = False


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Blog.objects.annotate(posts_count=Count('posts'))

    def post_count(self, obj):
        return obj.posts_count
    post_count.short_description = 'Post count'
    post_count.admin_order_field = "posts_count"

    list_display = ('title', 'post_count', 'created_date', 'last_modified')
    search_fields = ('title',)
    ordering = ('-created_date',)
    readonly_fields = ('created_date', 'last_modified')

    # Method to display posts in the admin change view
    def display_posts(self, obj):
        posts = obj.posts.all().order_by('-published_date')
        if not posts.exists():
            return "No posts yet."

        # Create a simple list of posts
        post_links = []
        for post in posts[:10]:  # Show first 10 posts
            admin_url = reverse('admin:blogs_post_change', args=[post.pk])
            post_link = format_html('<a href="{}" target="_blank">{}</a><br>',
                                   admin_url, escape(post.title or "Untitled"))
            post_links.append(post_link)

        if len(posts) > 10:
            post_links.append(f"... and {len(posts) - 10} more posts")

        return format_html(''.join(post_links))

    display_posts.short_description = 'Recent Posts'
    readonly_fields = ('created_date', 'last_modified', 'display_posts')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'publish', 'is_page', 'last_modified')
    search_fields = ('title', 'content')
    ordering = ('-published_date',)
    list_filter = ('publish', 'is_page')
    readonly_fields = ('uid', 'last_modified')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('url',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


admin.site.register(Stylesheet)

