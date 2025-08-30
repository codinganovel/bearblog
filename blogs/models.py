from django.utils import timezone
from django.db import models

from zoneinfo import ZoneInfo
import os
import json
from math import log
import random
import string
import hashlib
import requests


class Blog(models.Model):
    # Single blog instance - no user relationship needed
    title = models.CharField(max_length=200, default="My Blog")
    subdomain = models.SlugField(max_length=100, default="blog", db_index=True)
    auth_token = models.CharField(max_length=128, default="", blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)
    last_modified = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)
    last_posted = models.DateTimeField(blank=True, null=True, db_index=True)

    # Core blog content
    nav = models.TextField(default="[Home](/) [Blog](/blog/)", blank=True)
    content = models.TextField(default="Hello World!", blank=True)
    meta_description = models.CharField(max_length=200, blank=True)
    meta_image = models.CharField(max_length=200, blank=True)
    lang = models.CharField(max_length=10, default='en', blank=True, db_index=True)
    meta_tag = models.CharField(max_length=500, blank=True)
    blog_path = models.CharField(max_length=200, default="blog")
    header_directive = models.TextField(blank=True)
    footer_directive = models.TextField(blank=True)
    all_tags = models.TextField(default='[]')

    # Styling and customization
    custom_styles = models.TextField(blank=True)
    overwrite_styles = models.BooleanField(
        default=False,
        choices=((True, 'Overwrite default styles'), (False, 'Extend default styles')),
        verbose_name='')
    favicon = models.CharField(max_length=100, default="🐼", blank=True)
    optimise_images = models.BooleanField(default=True)
    date_format = models.CharField(max_length=32, default="d M, Y", blank=True)

    # Blog settings
    post_template = models.TextField(blank=True)
    robots_txt = models.TextField(blank=True, default="User-agent: *\nAllow: /")
    rss_alias = models.CharField(max_length=100, blank=True)
    codemirror_enabled = models.BooleanField(default=True)

        # Ensure only one blog instance exists
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blog"

    @property
    def contains_code(self):
        return "```" in self.content

    @property
    def is_empty(self):
        content_length = len(self.content) if self.content is not None else 0
        return content_length < 20 and self.posts.count() == 0 and self.custom_styles == ""
    
    @property
    def tags(self):
        return sorted(json.loads(self.all_tags))
    
    def update_all_tags(self):
        all_tags = []
        if self.pk:
            for post in Post.objects.filter(blog=self, publish=True, is_page=False, published_date__lt=timezone.now()):
                all_tags.extend(json.loads(post.all_tags))
                all_tags = list(set(all_tags))
        self.all_tags = json.dumps(all_tags)

    def save(self, *args, **kwargs):
        # Handle all tags
        self.update_all_tags()

        # When custom styles is empty set it to default (legacy overwrite patch)
        if not self.custom_styles:
            default_stylesheet = Stylesheet.objects.filter(identifier="default").first()
            if default_stylesheet:
                self.custom_styles = default_stylesheet.css
                self.overwrite_styles = True
            else:
                # Fallback to basic CSS if no default stylesheet exists
                self.custom_styles = """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}
a {
    color: #3498db;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
"""
                self.overwrite_styles = True

        if self.pk:
            # Update last posted
            self.last_posted = self.posts.filter(publish=True, published_date__lt=timezone.now()).order_by('-published_date').values_list('published_date', flat=True).first()

        # Save the blog
        super(Blog, self).save(*args, **kwargs)

    @property
    def useful_domain(self):
        """Return the domain for the personal CMS"""
        return "http://localhost:8000"
    
    @property
    def dynamic_useful_domain(self):
        """Return the domain for the personal CMS"""
        return "http://localhost:8000"
    
    @property
    def blank_useful_domain(self):
        """Return the domain without protocol"""
        return "localhost:8000"

    def __str__(self):
        return self.title


class Post(models.Model):
    # Single blog - no foreign key needed, we'll get blog from singleton
    uid = models.CharField(max_length=200, db_index=True)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.CharField(max_length=200, db_index=True)
    alias = models.CharField(max_length=200, blank=True, db_index=True)
    published_date = models.DateTimeField(blank=True, db_index=True)
    last_modified = models.DateTimeField(auto_now_add=True, blank=True)
    all_tags = models.TextField(default='[]')
    publish = models.BooleanField(default=True, db_index=True)
    is_page = models.BooleanField(default=False, db_index=True)
    content = models.TextField()
    canonical_url = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=200, blank=True)
    meta_image = models.CharField(max_length=200, blank=True)
    lang = models.CharField(max_length=10, blank=True, db_index=True)
    class_name = models.CharField(max_length=200, blank=True)

    @property
    def contains_code(self):
        return "```" in self.content

    @property
    def tags(self):
        return sorted(json.loads(self.all_tags))
    
    @property
    def token(self):
        return hashlib.sha256(self.uid.encode()).hexdigest()[0:10]

    def save(self, *args, **kwargs):
        self.slug = self.slug.lower()
        if not self.all_tags:
            self.all_tags = '[]'

        # Create unique random identifier
        if not self.uid:
            allowed_chars = string.ascii_letters.replace('O', '').replace('l', '')
            self.uid = ''.join(random.choice(allowed_chars) for _ in range(20))

        # Save the post
        super(Post, self).save(*args, **kwargs)

        # Update blog tags
        try:
            from .models import Blog
            blog = Blog.objects.first()
            if blog:
                blog.save()
        except:
            pass  # Handle case where blog doesn't exist yet

    def __str__(self):
        return self.title


class Stylesheet(models.Model):
    title = models.CharField(max_length=100)
    identifier = models.SlugField(max_length=100, unique=True)
    css = models.TextField(blank=True)
    external = models.BooleanField(default=False)
    image = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Media(models.Model):
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    @property
    def name(self):
        return self.url.split('/')[-1]

    def __str__(self):
        return f"{self.url} - {self.created_at}"
