import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# SECURITY
# ========================
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool) # Set to False for Production
ALLOWED_HOSTS = ALLOWED_HOSTS = [
    '.onrender.com',        # covers all render domains
    'localhost',
    '127.0.0.1',
    'chhohreivung.site',
    'www.chhohreivung.site'
]
# ========================
# INSTALLED APPS
# ========================
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',  # Must be at the top
    'cloudinary_storage',             # Must be above staticfiles
    'jazzmin',                        # Optional: Admin UI
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third Party
    'ckeditor',
    'ckeditor_uploader',
    'cloudinary',
    
    # Your Apps
    'blog',
]

# ========================
# MIDDLEWARE
# ========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Essential for Vercel CSS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_pach.urls'

# ========================
# STATIC FILES (Vercel + WhiteNoise)
# ========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# This specific path is required for the Vercel build script
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# WhiteNoise handles the CSS/JS compression and serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ========================
# MEDIA / CLOUDINARY (User Uploads)
# ========================
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}

# ========================
# DATABASE
# ========================
DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL'))
}

# ========================
# CKEDITOR CONFIG
# ========================
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_STORAGE_BACKEND = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ','.join(['codesnippet', 'uploadimage']),
    },
}

# ========================
# TEMPLATES & OTHER DEFAULTS
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
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True