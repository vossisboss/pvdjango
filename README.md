# Step Two: Install and configure Wagtail Localize

Wagtail Localize is a package that will help you set up a translation workflow for your website. It provides a few different options for translation workflows, but one of the most useful features is the ability to sync content from the main language to other languages.

For this tutorial, we're going to use Wagtail 4.0 and an alpha version of Wagtail Localize. To install that version of Wagtail Localize, enter the following command in your command line:

```
pip install wagtail-localize==1.3a4
```

## But first, a quick bug fix

Before we install Wagtail Localize, you'll need to change a migration because there is currently a bug that creates a table conflict in the database with Wagtail Localize. To prevent that headache, execute these commands in your terminal

```
python manage.py migrate wagtailcore 0058
python manage.py migrate
```

These commands revert the `wagtailcore 0059` migration back to `wagtailcore 0058` to prevent the table conflict from occurring. This step should hopefully be unnecessary after the bug is fixed.

With that fixed, now you are going to make some changes to `base.py` and `urls.py`. Most of the steps you're going to perform next come from the [Wagtail Localize documentation](https://www.wagtail-localize.org/). 


## Add Wagtail Localize to INSTALLED_APPS


Go to `myblog\settings\base.py` and open the file in your text editor or IDE. Find the `INSTALLED_APPS` setting, and insert `'wagtail_localize'` and `'wagtail_localize.locales'` in between
`'search` and `'wagtail.contrib.forms'`:

```python
INSTALLED_APPS = [
    "home",
    "search",
    # Insert these here
    "wagtail_localize",
    "wagtail_localize.locales",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    # ...
]
```

Note that the `wagtail_localize.locales` module is a temporary replacement for Wagtail's builtin `wagtail.locales`
module.

## Enable internationalization in Wagtail

Find the "Internationalisation" section, and add the `WAGTAIL_I18N_ENABLED` setting:

```python
USE_I18N = True

USE_L10N = True

# Add this
WAGTAIL_I18N_ENABLED = True

USE_TZ = True
```

## Configure languages


In the "Internationalisation" section, add the following to set the `LANGUAGES` and `WAGTAIL_CONTENT_LANGUAGES`
settings to English and French:

```python
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ("en", "English"),
    ("fr", "French"),
]
```

## Add machine translation configuration

Wagtail Localize has a few different options for machine translation. Two common configurations are for Google Cloud Translation and Deepl. Both of those options require setting accounts up with credit cards, so were going to use the dummy translator for this tutorial to show you how things work. But if you want to integrate a machine translator, you can follow the steps in the [Wagtail Localize Documentation](https://www.wagtail-localize.org/how-to/integrations/machine-translation/) to add the configuration for your preferred translator to `base.py`. There is also an integration available for [Pontoon](https://www.wagtail-localize.org/how-to/integrations/pontoon/).

To add the dummy translator, add the following code to your `base.py` file:

```
WAGTAILLOCALIZE_MACHINE_TRANSLATOR = {
    "CLASS": "wagtail_localize.machine_translators.dummy.DummyTranslator",
}
```

## Enable `LocaleMiddleware`

Django's `LocaleMiddleware` detects a user's browser language and forwards them to the most appropriate language
version of the website.

To enable it, insert `'django.middleware.locale.LocaleMiddleware'` into the middleware setting
above `RedirectMiddleware`:

```python
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # Insert this here
    "django.middleware.locale.LocaleMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]
```
## Configure URL paths

Next, you need configure which URL paths are translatable so that Django will prefix them with the language code.

Open `tutorial/urls.py` in your text editor. You'll see that there are two groups of URL patterns with an
`if settings.DEBUG:` block in between them.

The patterns that need to be made translatable are:

- `path('search/', search_views.search, name='search'),`
- `path("", include(wagtail_urls)),`

To make these translatable, move the 'search/' pattern into the second block, above the `wagtail_urls` pattern. Then,
replace the square brakets around that block with
[`i18n_patterns`](https://docs.djangoproject.com/en/3.1/topics/i18n/translation/#django.conf.urls.i18n.i18n_patterns):

```python
from django.conf.urls.i18n import i18n_patterns


# These paths are translatable so will be given a language prefix (eg, '/en', '/fr')
urlpatterns = urlpatterns + i18n_patterns(
    path("search/", search_views.search, name="search"),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
)
```

With the search pattern removed, the first group should now look like:

```python
# These paths are non-translatable so will not be given a language prefix
urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
]
```

## Migrate the database

Run the migrate command again to set up the tables for Wagtail Localize in the database:

```
python manage.py migrate
```

## Check your site


Go back to `http://127.0.0.1:8000`. If your browser is configured for English or any other language except French,
you should be redirected to `http://127.0.0.1:8000/en/`.
If your browser is configured in French, you should be redirected to `http://127.0.0.1:8000/fr/`.

In either case, you can view the site in `/en/` or `/fr/` (no differences yet).

If this is all working as described, that means `i18n_patterns` and `LocaleMiddleware` are working!