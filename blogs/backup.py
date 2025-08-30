from django.utils import timezone
import os
import json
from threading import Thread


def backup_in_thread(blog):
    """Simplified backup function for personal CMS"""
    print(f"Backing up {blog.title} in thread")
    thread = Thread(target=backup_blog, args=(blog,))
    thread.start()
    return thread


def backup_blog(blog):
    """Simple backup function that saves to local files"""
    try:
        date_str = timezone.now().strftime('%Y-%m-%d')
        backup_dir = os.path.join('backups', date_str)
        os.makedirs(backup_dir, exist_ok=True)

        # Save blog data
        blog_data = {
            'title': blog.title,
            'content': blog.content,
            'meta_description': blog.meta_description,
            'created_date': blog.created_date.isoformat(),
            'last_modified': blog.last_modified.isoformat(),
        }

        with open(os.path.join(backup_dir, 'blog.json'), 'w') as f:
            json.dump(blog_data, f, indent=2)

        # Save posts data
        posts_data = []
        for post in blog.posts.all():
            posts_data.append({
                'title': post.title,
                'slug': post.slug,
                'content': post.content,
                'published_date': post.published_date.isoformat() if post.published_date else None,
                'publish': post.publish,
                'is_page': post.is_page,
            })

        with open(os.path.join(backup_dir, 'posts.json'), 'w') as f:
            json.dump(posts_data, f, indent=2)

        return {
            'success': True,
            'backup_date': date_str,
            'post_count': len(posts_data)
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
