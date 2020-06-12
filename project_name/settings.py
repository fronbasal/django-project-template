import os

from configurations import Configuration, values


class Common(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    SECRET_KEY = values.SecretValue()
    DEBUG = values.BooleanValue(False)
    ALLOWED_HOSTS = values.ListValue([])
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "whitenoise.runserver_nostatic",
        "django.contrib.staticfiles",

        'rest_framework',
        "django_extensions",
        "debug_toolbar",

        'django_celery_results',
        'django_celery_beat',

        "{{ project_name }}.users",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "{{ project_name }}.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "{{ project_name }}.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases
    DATABASES = values.DatabaseURLValue(
        "sqlite:///{}".format(os.path.join(BASE_DIR, "db.sqlite3"))
    )

    # Password validation
    # https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/
    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    AUTH_USER_MODEL = "users.User"

    CELERY_RESULT_BACKEND = 'django-db'
    CELERY_CACHE_BACKEND = 'django-cache'


class Development(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True

    ALLOWED_HOSTS = []

    INTERNAL_IPS = [
        "127.0.0.1"
    ]

    MIDDLEWARE = Common.MIDDLEWARE + [
        "debug_toolbar.middleware.DebugToolbarMiddleware"
    ]


class Staging(Common):
    """
    The in-staging settings.
    """
    # Security
    SESSION_COOKIE_SECURE = values.BooleanValue(False)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(False)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(False)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(False)
    SECURE_HSTS_SECONDS = values.IntegerValue(31536000)
    SECURE_REDIRECT_EXEMPT = values.ListValue(["localhost", "127.0.0.1"])
    SECURE_SSL_HOST = values.Value(None)
    SECURE_SSL_REDIRECT = values.BooleanValue(False)
    SECURE_PROXY_SSL_HEADER = values.TupleValue(
        ("HTTP_X_FORWARDED_PROTO", "https")
    )

    DATABASES = values.DatabaseURLValue("postgresql://pg:pg@postgres/pg")


class Production(Staging):
    """
    The in-production settings.
    """
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_HSTS_SECONDS = values.IntegerValue(31536000)
    SECURE_REDIRECT_EXEMPT = values.ListValue(["localhost", "127.0.0.1"])
    SECURE_SSL_HOST = values.Value(None)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
