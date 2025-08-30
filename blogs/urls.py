from django.urls import path

from blogs.views import blog, dashboard, studio, feed, analytics, emailer, media

urlpatterns = [
    path('', blog.home, name='home'),

    # Admin/Dashboard (simplified for single blog)
    path('dashboard/', studio.studio, name="dashboard"),
    path('dashboard/nav/', dashboard.nav, name='nav'),
    path('dashboard/styles/', dashboard.styles, name='styles'),
    path('dashboard/settings/', dashboard.settings, name='settings'),
    path('dashboard/settings/advanced/', studio.advanced_settings, name='advanced_settings'),
    path('dashboard/directives/', studio.directive_edit, name="directive_edit"),

    # Media
    path('dashboard/media/', media.media_center, name='media_center'),
    path('dashboard/media/delete-selected/', media.delete_selected_media, name='delete_selected_media'),
    path('dashboard/upload-image/', media.upload_image, name='upload_image'),
    path('media/<str:img>/', media.image_proxy, name="image-proxy"),

    # Analytics (simplified)
    path('dashboard/analytics/', analytics.analytics, name='analytics'),

    # Posts and Pages
    path('dashboard/posts/', dashboard.posts_edit, name='posts_edit'),
    path('dashboard/pages/', dashboard.pages_edit, name='pages_edit'),
    path('dashboard/posts/new/', studio.post, name="post_new"),
    path('dashboard/posts/<uid>/', studio.post, name="post_edit"),
    path('dashboard/posts/<uid>/delete/', dashboard.post_delete, name='post_delete'),
    path('dashboard/preview/', studio.preview, name="post_preview"),
    path('dashboard/post-template/', studio.post_template, name="post_template"),

    # Blog
    path('sitemap.xml', blog.sitemap, name='sitemap'),
    path('robots.txt', blog.robots, name='robots'),

    # Feeds + aliases
    path("feed/", feed.feed),
    path("atom/", feed.feed),
    path("rss/", feed.feed),
    path("feed/atom/", feed.feed),
    path("feed/rss/", feed.feed),
    path("feed.xml", feed.feed),
    path("atom.xml", feed.feed),
    path("rss.xml", feed.feed),
    path("index.xml", feed.feed),

    # Generic path endpoint for slugs
    path('<path:slug>/', blog.post, name='post'),
]
