from django.utils import timezone
from django.core.mail import send_mail, get_connection, EmailMultiAlternatives
from django.conf import settings
from django.db import connection
from django.utils.text import slugify

import re
import string
import os
import random
import threading
from requests.exceptions import ConnectionError, ReadTimeout
import requests
import subprocess
from datetime import timedelta
from time import time
import hashlib

from blogs.models import Post


def is_protected(subdomain):
    protected_subdomains = [
        'login',
        'mg',
        'www',
        'api',
        'signup',
        'signin',
        'profile',
        'register',
        'post',
        'http',
        'https',
        'account',
        'router',
        'settings',
        'support',
        'eng',
        'admin',
        'dashboard',
        'mail',
        'static',
        'blog',
        'dev',
        'beta',
        'staging',
        'secure',
        'user',
        'portal',
        'help',
        'contact',
        'news',
        'media',
        'docs',
        'auth',
        'status',
        'assets',
        'bearblog.dev',
        '*.bearblog.dev',
        'router.bearblog.dev',
        'www.bearblog.dev',
        '_dmarc',
        'domain-proxy'
    ]

    return subdomain in protected_subdomains


def check_records(domain):
    if not domain:
        return
    verification_string = subprocess.Popen(["dig", "-t", "txt", domain, '+short'], stdout=subprocess.PIPE).communicate()[0]
    return ('look-for-the-bear-necessities' in str(verification_string))


def check_connection(blog):
    if not blog.domain:
        return
    else:
        try:
            response = requests.request("GET", blog.useful_domain, allow_redirects=False, timeout=10)
            return (f'<meta name="{ blog.subdomain }" content="look-for-the-bear-necessities">' in response.text)
        except ConnectionError:
            return False
        except ReadTimeout:
            return False
        except SystemExit:
            return False


def create_cache_key(host, path=None, tag=None):
    cache_key = host.replace('.', '_')
    if path:
        cache_key += f"_{path}"
    if tag:
        cache_key += f"_{tag}" 
    cache_key = slugify(cache_key).replace('-', '_')

    return cache_key


def pseudo_word(length=5):
    vowels = "aeiou"
    consonants = "".join(set(string.ascii_lowercase) - set(vowels))
    
    word = ""
    for i in range(length):
        if i % 2 == 0:
            word += random.choice(consonants)
        else:
            word += random.choice(vowels)
    
    return word


def salt_and_hash(request, duration='day'):
    """Simplified hashing function - removed ipaddr dependency"""
    # For personal CMS, use a simple hash based on timestamp
    if duration == 'year':
        date_part = timezone.now().year
    else:
        date_part = timezone.now().date()

    hash_string = f"anonymous-{date_part}-{os.getenv('SECRET_KEY', 'default-salt')}"
    hash_id = hashlib.sha256(hash_string.encode('utf-8')).hexdigest()

    return hash_id


def get_country(user_ip):
    """Simplified country detection - removed geoip2 dependency"""
    # For personal CMS, we'll just return empty dict
    # GeoIP functionality removed to simplify deployment
    return {'country_name': 'Unknown'}


def unmark(content):
    content = re.sub(r'^\s{0,3}#{1,6}\s+.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s{0,3}[-*]{3,}\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s{0,3}>\s+.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`]+`', '', content)
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    content = re.sub(r'\[.*?\]\(.*?\)', '', content)
    content = re.sub(r'(\*\*|__)(.*?)\1', '', content)
    content = re.sub(r'(\*|_)(.*?)\1', '', content)
    content = re.sub(r'~~.*?~~', '', content)
    content = re.sub(r'^\s{0,3}[-*+]\s+.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s{0,3}\d+\.\s+.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*\|.*?\|\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*[:-]{3,}\s*$', '', content, flags=re.MULTILINE)

    return content


def clean_text(text):
    return ''.join(c for c in text if valid_xml_char_ordinal(c))


def valid_xml_char_ordinal(c):
    codepoint = ord(c)
    # conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
    )


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, connection=None):
    connection = connection or get_connection(username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


class EmailThread(threading.Thread):
    def __init__(self, subject, html_message, from_email, recipient_list):
        self.subject = subject
        self.html_message = html_message
        self.from_email = from_email
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.html_message,
            self.from_email,
            self.recipient_list,
            fail_silently=True,
            html_message=self.html_message)


def send_async_mail(subject, html_message, from_email, recipient_list):
    if settings.DEBUG:
        print(html_message)
    else:
        print('Sent email to ', recipient_list)
        EmailThread(subject, html_message, from_email, recipient_list).start()


def random_post_link():
    """Get a random published post link - simplified for single blog"""
    posts = Post.objects.filter(
        publish=True,
        published_date__lte=timezone.now(),
        content__isnull=False
    )

    if posts.exists():
        count = posts.count()
        random_index = random.randint(0, count - 1)
        post = posts[random_index]
        return f"/{post.slug}/"

    return "/"
