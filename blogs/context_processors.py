import os

# Add tz and admin_passport to every page
def extra(request):
    main_site_hosts = os.getenv('MAIN_SITE_HOSTS', 'localhost:8000')
    if main_site_hosts:
        bear_root = 'http://' + main_site_hosts.split(',')[0]
    else:
        bear_root = 'http://localhost:8000'

    return {
        'tz': request.COOKIES.get('timezone', 'UTC'),
        'admin_passport': request.COOKIES.get('admin_passport') == os.getenv('ADMIN_PASSPORT'),
        'bear_root': bear_root
    }
