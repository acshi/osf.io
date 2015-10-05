"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
from urlparse import urlparse
from website import settings as osf_settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = osf_settings.SECRET_KEY

AUTHENTICATION_BACKENDS = (
    'api.base.authentication.backends.ODMBackend',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = osf_settings.DEBUG_MODE

ALLOWED_HOSTS = [
    '.osf.io'
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',
    'raven.contrib.django.raven_compat',
)

# TODO: Are there more granular ways to configure reporting specifically related to the API?
RAVEN_CONFIG = {
    'dsn': osf_settings.SENTRY_DSN
}

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_BULK_LIMIT': 10,

    # Order is important here because of a bug in rest_framework_swagger. For now,
    # rest_framework.renderers.JSONRenderer needs to be first, at least until
    # https://github.com/marcgibbons/django-rest-swagger/issues/271 is resolved.
    'DEFAULT_RENDERER_CLASSES': (
        'api.base.renderers.JSONAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        'api.base.renderers.BrowsableAPIRendererNoForms',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'api.base.parsers.JSONAPIParser',
        'api.base.parsers.JSONAPIParserForRegularJSON',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'EXCEPTION_HANDLER': 'api.base.exceptions.json_api_exception_handler',
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'api.base.content_negotiation.JSONAPIContentNegotiation',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': '2.0',
    'DEFAULT_FILTER_BACKENDS': ('api.base.filters.ODMOrderingFilter',),
    'DEFAULT_PAGINATION_CLASS': 'api.base.pagination.JSONAPIPagination',
    'ORDERING_PARAM': 'sort',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Custom auth classes
        'api.base.authentication.drf.OSFBasicAuthentication',
        'api.base.authentication.drf.OSFSessionAuthentication',
        'api.base.authentication.drf.OSFCASAuthentication'
    ),
}

# Settings related to CORS Headers addon: allow API to receive authenticated requests from OSF
# CORS plugin only matches based on "netloc" part of URL, so as workaround we add that to the list
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (urlparse(osf_settings.DOMAIN).netloc,
                         osf_settings.DOMAIN,
                         )
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE_CLASSES = (
    # TokuMX transaction support
    # Needs to go before CommonMiddleware, so that transactions are always started,
    # even in the event of a redirect. CommonMiddleware may cause other middlewares'
    # process_request to be skipped, e.g. when a trailing slash is omitted
    'api.base.middleware.DjangoGlobalMiddleware',
    'api.base.middleware.TokuTransactionsMiddleware',

    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True
    }]


ROOT_URLCONF = 'api.base.urls'
WSGI_APPLICATION = 'api.base.wsgi.application'


LANGUAGE_CODE = 'en-us'

# Disabled to make a test work (TestNodeLog.test_formatted_date)
# TODO Try to understand what's happening to cause the test to break when that line is active.
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static/vendor')

API_BASE = 'v2/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    ('rest_framework_swagger/css', os.path.join(BASE_DIR, 'static/css')),
    ('rest_framework_swagger/images', os.path.join(BASE_DIR, 'static/images')),
)

# TODO: Revisit methods for excluding private routes from swagger docs
SWAGGER_SETTINGS = {
    'info': {
        'api_path': '/',
        'description':
        """
        <p>Welcome to the V2 Open Science Framework API. With this API you can programatically access users,
        projects, components, and files from the <a href="https://osf.io/">Open Science Framework</a>. The Open Science
        Framework (OSF) is a free, open-source service maintained by the <a href="https://cos.io/">Center for Open Science</a>. </p>
        <p> The OSF stores, documents, and archives study designs, materials, data, manuscripts, or anything else associated
        with your research during the research process. Every project and file on the OSF has a permanent unique
        identifier, and every registration (a permanent, time-stamped version of your projects and files) can be assigned
        a DOI/ARK. You can use the OSF to measure your impact by monitoring the traffic to projects and files you make
        public. With the OSF you have full control of what parts of your research are public and what remains private.</p>
        <p>Beta notice: This API is currently a beta service.  You are encouraged to use the API and will receive support
        when doing so, however, while the API remains in beta status, it may change without notice as a result of
        product updates. The temporary beta status of the API will remain in place while it matures. In a future
        release, the beta status will be removed, at which point we will provide details on how long we will support
        the API V2 and under what circumstances it might change.</p>
         <h2>General API Usage</h2>
        <p> Each endpoint will have its own documentation, but there are some general principles.</p>
        <h3>Filtering</h3>
        <p> Collections can be filtered by adding a query parameter in the form:</p>
        <pre>filter[&lt;fieldname&gt;]=&lt;matching information&gt;</pre>
        <p>For example, if you were trying to find <a href="http://en.wikipedia.org/wiki/Lise_Meitner">Lise Meitner</a>:</p>
        <pre>/users?filter[full_name]=meitn</pre>
        <p>You can filter on multiple fields, or the same field in different ways, by &-ing the query parameters together.</p>
        <pre>/users?filter[full_name]=lise&filter[family_name]=mei</pre>
        <h3>Links</h3>
        <p> Responses will generally have associated links which are helpers to keep you from having to construct URLs in
        your code or by hand. If you know the route to a high-level resource, you can go to that route. For example:</p>
        <pre>/nodes/&lt;node_id&gt;</pre>
        <p> is a good route to create rather than going to /nodes/ and navigating by id filtering. However, if you are
        creating something that crawls the structure of a node going to the child node or gathering children,
        contributors, and similar related resources, then take the link from the object you\'re crawling rather than
        constructing the link yourself.
        In general, links include:</p>
        <ol>
        <li>1. "Related" links, which will give you detailed information on individual items or a collection of related resources;</li>
        <li>2. "Self" links, which are used for general REST operations (POST, DELETE, and so on);</li>
        <li>3. Pagination links such as "next", "prev", "first", and "last". Pagination links are great for navigating long lists of
        information.</li></ol>
        <p> Some routes may have extra rules for links, especially if those links work with external services. Collections
        may have counts with them to indicate how many items are in that collection.</p>""",
        'title': 'OSF API Documentation',
    },
    'doc_expansion': 'list',
}
