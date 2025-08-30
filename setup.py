#!/usr/bin/env python3
"""
Setup script for Personal CMS (formerly BearBlog)
This script helps you get started with your personal blog quickly.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✓ Done")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_env_file():
    """Create a basic .env file with default settings"""
    env_content = """# Personal CMS Configuration
DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite by default)
# DATABASE_URL=sqlite:///db.sqlite3

# Email settings (optional)
# DEFAULT_FROM_EMAIL=noreply@yourblog.com
# SERVER_EMAIL=admin@yourblog.com
# EMAIL_HOST=smtp.gmail.com
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
"""

    env_file = Path('.env')
    if not env_file.exists():
        print("\nCreating .env file...")
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✓ Created .env file with default settings")
        print("  Please edit .env to configure your settings")
    else:
        print("✓ .env file already exists")

def setup_database():
    """Set up the database"""
    print("\nSetting up database...")
    if run_command("python3 manage.py migrate", "Running database migrations"):
        print("✓ Database setup complete")
        return True
    return False

def create_admin_user():
    """Create an admin user"""
    print("\nCreating admin user...")
    print("You'll be prompted to create an admin user for accessing the dashboard.")

    try:
        subprocess.run(["python3", "manage.py", "createsuperuser"], check=True)
        print("✓ Admin user created")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to create admin user")
        return False

def create_sample_content():
    """Create sample blog content"""
    print("\nCreating sample blog content...")

    sample_script = """
import os
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
django.setup()

from blogs.models import Blog, Post, Stylesheet

# Create default blog if it doesn't exist
blog, created = Blog.objects.get_or_create(
    defaults={
        'title': 'My Personal Blog',
        'content': '''# Welcome to My Personal Blog

This is your personal blog powered by the Personal CMS. You can customize this content in the dashboard.

## Getting Started

1. Visit `/dashboard/` to access the admin panel
2. Create your first post
3. Customize your blog settings
4. Add pages and media

Happy blogging! 🐼
'''
    }
)

if created:
    print("Created default blog")
else:
    print("Blog already exists")

# Create default stylesheet if it doesn't exist
Stylesheet.objects.get_or_create(
    identifier='default',
    defaults={
        'title': 'Default Theme',
        'css': '''
/* Default theme styles */
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

.post {
    margin-bottom: 2em;
    border-bottom: 1px solid #eee;
    padding-bottom: 2em;
}

.post-meta {
    color: #666;
    font-size: 0.9em;
    margin-bottom: 1em;
}

.btn {
    display: inline-block;
    padding: 8px 16px;
    background: #3498db;
    color: white;
    border-radius: 4px;
    text-decoration: none;
}

.btn:hover {
    background: #2980b9;
}
'''
    }
)

# Create sample post
sample_post, created = Post.objects.get_or_create(
    uid='sample-post',
    defaults={
        'title': 'Welcome to Personal CMS',
        'slug': 'welcome-to-personal-cms',
        'content': '''# Welcome to Personal CMS

This is a sample blog post to get you started.

## Features

- **Simple blogging**: Write posts in Markdown
- **Custom themes**: Customize your blog's appearance
- **Media management**: Upload images and files
- **SEO friendly**: Built-in SEO optimization
- **Fast and lightweight**: No JavaScript bloat

## Next Steps

1. **Customize your blog**: Go to `/dashboard/` and update your blog settings
2. **Write your first post**: Click "New Post" in the dashboard
3. **Add a custom domain**: Configure your domain settings
4. **Upload media**: Add images to your posts

Enjoy your new personal blog! 🎉
''',
        'publish': True,
        'is_page': False,
    }
)

if created:
    print("Created sample post")
else:
    print("Sample post already exists")
"""

    with open('create_sample.py', 'w') as f:
        f.write(sample_script)

    try:
        subprocess.run(['python3', 'create_sample.py'], check=True)
        print("✓ Sample content created")
        os.remove('create_sample.py')
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create sample content: {e}")
        if os.path.exists('create_sample.py'):
            os.remove('create_sample.py')
        return False

def main():
    """Main setup function"""
    print("🐼 Personal CMS Setup")
    print("=" * 50)

    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("✗ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)

    # Create .env file
    create_env_file()

    # Install dependencies
    if not run_command("python3 -m pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)

    # Setup database
    if not setup_database():
        sys.exit(1)

    # Create admin user
    if not create_admin_user():
        print("⚠ Warning: Admin user creation failed. You can create one later with:")
        print("   python manage.py createsuperuser")

    # Create sample content
    if not create_sample_content():
        print("⚠ Warning: Sample content creation failed.")

    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Run: python3 manage.py runserver")
    print("2. Visit: http://localhost:8000")
    print("3. Access dashboard: http://localhost:8000/dashboard/")
    print("4. Login with your admin credentials")
    print("\nFor production deployment:")
    print("- Set DEBUG=False in .env")
    print("- Configure ALLOWED_HOSTS")
    print("- Set up a proper web server (nginx, etc.)")
    print("- Consider using Docker for deployment")

if __name__ == '__main__':
    main()
