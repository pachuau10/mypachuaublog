"""
Django settings for blog_pach project.
"""


import csv
from pathlib import Path
import os
from decouple import config,Csv
import dj_database_url
import cloudinary



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# SECURITY
# ========================
SECRET_KEY = config('SECRET_KEY', default='your-default-secret-key')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = [ 
    '.vercel.app', 
    'now.sh', 
    'localhost', 
    '127.0.0.1',
    'chhohreivung.site',           # Your domain
    'www.chhohreivung.site' ]
# ========================
# INSTALLED APPS
# ========================
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor_uploader', 
    'codemirror2',
    'blog',
    'ckeditor',
    'cloudinary',
    'cloudinary_storage',
]

JAZZMIN_SETTINGS = {
    "site_title": "My Blog Admin",
    "site_header": "Blog Administration",
    "welcome_sign": "Welcome to your Admin Panel",
    "site_logo": "static/images/profileduha.jpg", 
    "copyright": "MyBlog 2025",
    "show_ui_builder": True,  
        "icons": {
        "blog.Category": "fas fa-tag",
        "blog.BlogPost": "fas fa-newspaper",
        "blog.Newsletter": "fas fa-envelope-open",
        "blog.ContactMessage": "fas fa-comment",
    }
}


# Required: Upload path for CKEditor
CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/"

# CKEditor custom configurations
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['Link', 'Unlink', 'Anchor'],
            ['RemoveFormat', 'Source'],
            ['Image', 'Table', 'HorizontalRule'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize'],
            ['CodeSnippet'], 
        ],
        'height': 400,
        'width': '100%',

        'extraPlugins': ','.join([
            'uploadimage',
            'image2',
            'codesnippet',       # REQUIRED FOR CODE EDITOR
        ]),

        'codeSnippet_theme': 'monokai_sublime',

        'filebrowserUploadUrl': '/ckeditor/upload/',
        'filebrowserBrowseUrl': '/ckeditor/browse/',
        'removePlugins': 'image',
        'image2_alignClasses': ['image-align-left', 'image-align-center', 'image-align-right'],
    },
}

# Security settings for CKEditor
CKEDITOR_ALLOW_NONIMAGE_FILES = False  # Only allow images
CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_RESTRICT_BY_DATE = False

CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_STORAGE_BACKEND = 'blog.storage.CKEditorCloudinaryStorage'
# ========================
# MIDDLEWARE
# ========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_pach.urls'

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS', 
    default='https://chhohreivung.site,https://www.chhohreivung.site',
    cast=Csv()
)

# ========================
# TEMPLATES
# ========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog_pach.wsgi.application'

# ========================
# DATABASE (PostgreSQL Neon)
# ========================
DATABASES = {
    'default': dj_database_url.parse(
        config(
            'DATABASE_URL',
            default='postgresql://user:password@localhost/dbname'
        )
    )
}

# ========================
# PASSWORD VALIDATORS
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ========================
# INTERNATIONALIZATION
# ========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ========================
# STATIC FILES
# ========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# --- FIX: Use Cloudinary for serving static files in production ---
# This ensures that files like /static/admin/css/base.css are found on the CDN.
# settings.py - Ensure this conditional logic is present!
if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticCloudinaryStorage'

if not DEBUG:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
# ========================
# MEDIA / CLOUDINARY
# ========================
MEDIA_URL = '/media/'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}

#Configure the native Cloudinary library for template tags 
cloudinary.config( 
    cloud_name = config('CLOUDINARY_CLOUD_NAME'), 
    api_key = config('CLOUDINARY_API_KEY'), 
    api_secret = config('CLOUDINARY_API_SECRET'),
    secure = True # Recommended to use HTTPS
)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# ========================
# DEFAULT PRIMARY KEY
# ========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'