# 🐼 Personal CMS

A simple, fast, and self-hostable personal blogging platform. Write in Markdown, customize your theme, and deploy anywhere.

## ✨ Features

- **Simple blogging**: Write posts in Markdown, no complex editors
- **Custom themes**: Customize your blog's appearance with CSS
- **Media management**: Upload and manage images
- **SEO friendly**: Built-in SEO optimization
- **Fast and lightweight**: No JavaScript bloat or trackers
- **Self-hostable**: Deploy on any server or cloud platform
- **Docker support**: Easy deployment with Docker

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd personal-cms

# Run the setup script
python setup.py
```

The setup script will:
- Create a `.env` configuration file
- Install dependencies
- Set up the database
- Create an admin user
- Add sample content

### Option 2: Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run the server
python manage.py runserver
```

### Option 3: Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t personal-cms .
docker run -p 8000:8000 personal-cms
```

## 📝 Usage

### Accessing the Dashboard

1. Visit `http://localhost:8000/dashboard/`
2. Login with your admin credentials
3. Start creating posts and customizing your blog

### Creating Posts

1. Go to Dashboard → Posts → New Post
2. Write in Markdown (see [Markdown Guide](#markdown-guide))
3. Set publish status and publish date
4. Save and preview

### Customizing Your Blog

1. Dashboard → Settings
2. Update blog title, description, and appearance
3. Customize CSS for unique styling
4. Upload a favicon and meta images

## 🎨 Customization

### Themes

The CMS comes with a default clean theme. You can customize it by:

1. **CSS Customization**: Edit the custom styles in Dashboard → Settings
2. **Theme Variables**: Override default colors and fonts
3. **Layout Options**: Choose between different layout styles

### Advanced Customization

For advanced customization, you can modify:
- `templates/` - HTML templates
- `static/` - CSS, images, and other assets
- `blogs/views/` - Python view logic

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database (SQLite by default)
# DATABASE_URL=postgresql://user:password@localhost/dbname

# Email settings (optional)
DEFAULT_FROM_EMAIL=noreply@yourblog.com
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Production Deployment

For production deployment:

1. Set `DEBUG=False`
2. Configure `ALLOWED_HOSTS`
3. Use a production web server (nginx, Apache)
4. Set up SSL certificates
5. Use environment variables for secrets

## 📚 Markdown Guide

Personal CMS supports standard Markdown with some extensions:

### Basic Syntax

```markdown
# Heading 1
## Heading 2
### Heading 3

**Bold text**
*Italic text*
~~Strikethrough~~

- Bullet list
- Another item

1. Numbered list
2. Another item

[Link text](https://example.com)
![Alt text](image-url.jpg)

> Blockquote

`inline code`

```language
Code block
```
```

### Extended Features

- **Tables**: Full table support
- **Footnotes**: Reference-style footnotes
- **Task Lists**: GitHub-style checkboxes
- **Code Highlighting**: Syntax highlighting for code blocks
- **Math**: LaTeX math expressions (optional)

## 🐳 Docker Deployment

### Development

```bash
# Run in development mode
docker-compose up
```

### Production

```bash
# Build for production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Docker Compose Configuration

The `docker-compose.yml` includes:
- **Web service**: Django application
- **Database**: SQLite (easily switchable to PostgreSQL)
- **Nginx**: Reverse proxy for production

## 📁 Project Structure

```
personal-cms/
├── blogs/                 # Main Django app
│   ├── models.py         # Database models
│   ├── views/            # View functions
│   ├── templates/        # HTML templates
│   └── static/           # CSS, JS, images
├── conf/                 # Django configuration
│   ├── settings.py       # Main settings
│   └── urls.py          # URL routing
├── static/               # Static files
├── templates/            # Base templates
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── requirements.txt     # Python dependencies
└── setup.py            # Setup script
```

## 🔌 API

Personal CMS provides a simple REST API for posts:

### Endpoints

- `GET /feed/` - RSS/Atom feed
- `GET /sitemap.xml` - XML sitemap
- `GET /api/posts/` - JSON API for posts

## 🤝 Contributing

This is a personal CMS focused on simplicity. For contributions:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. See LICENSE.md for details.

## 🆘 Support

- **Documentation**: Check the `/docs/` directory
- **Issues**: Use GitHub issues for bugs and features
- **Discussions**: Use GitHub discussions for questions

## 🙏 Acknowledgments

Originally based on BearBlog, transformed into a self-hostable personal CMS.

---

Happy blogging! 🐼
