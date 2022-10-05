# Parlez-vous Django? Internatiionalization with Wagtail

## What you should know

To complete this tutorial, you should be familiar with the following:

- Writing Python code
- Entering commands and in the command line

While it's not strictly necessary, you might find that you'll get more out of this tutorial if you complete the [introductory Django tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/) first.

## Prerequisites

To complete this tutorial, you will need:

- Python 3.8 or greater
- Git 
- A text editor or IDE
- A GitHub account (required for GitPod)
- Any web browser

# Step One: Set up Wagtail

## Create a virtual environment

### _Gitpod_

If you don't have Python already installed on your machine or if you would prefer not to troubleshoot environment issues, then you can complete this workshop in Gitpod. You will have to be more careful about saving your work since Gitpod environments deactivate after a period of inactivity.

Click the button below to launch Gitpod.

**NOTE**: A GitHub account is required to use Gitpod

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/vossisboss/pvdjango-gitpod)

### _Venv_

If you already have Python installed on your machine, you can create a local virtual environment using `venv`. Open your command line andnavigate to the directory you want to build your project in. Then enter the following commands to creative a virtual environment.

```
python 
python -m venv env
source env/bin/activate
```

## Set up Wagtail

Once you have a virtual environment set up, we can install Wagtail and start setting up our very first Wagtail website. In your project directory, enter the following command in your command line:

```
pip install wagtail
```

This command tells the Python package manager pip to install the latest release of Wagtail along with all of the dependencies that are needed for Wagtail. After Wagtail is installed, you can confirm that it is installed with:

```
pip show wagtail
```

After Wagtail is installed, you can use one of Wagtail's built-in commands to start a brand new website. For this tutorial, we're going to be creating a mini-blog project called `myblog`.

```
wagtail start myblog .
```

Don't forget the `.` at the end of the command. It is telling Wagtail to put all of the files in the current working directory.

Once all of the files are set up, you'll need to enter some commands to set up the test database and all of the migration files that Wagtail needs. You can do that with the `migrate` command.

```
python manage.py migrate
```

After the migrations are complete, you'll need to create a superuser so that you can access the backend of your Wagtail website. Use the following command:

```
python manage.py createsuperuser
```
Follow the prompts in your command line to create your superuser. Once you have a superuser set up, you can start up the test server to see your new Wagtail site in action.

```
python manage.py runserver
```
If the server has started up without any errors, you can navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000 ) in your web browser to see your Wagtail website. If you've successfully installed Wagtail, you should see a home page with a large teal egg on it.

To test that your superuser works, navigate to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and login with the credentials you created.

Now you have a basic Wagtail website set up. Next, we're going to add a package that will help you organize and translate content across different languages and locales.

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


Go back to `http://localhost:8000`. If your browser is configured for English or any other language except French,
you should be redirected to `http://localhost:8000/en/`.
If your browser is configured in French, you should be redirected to `http://localhost:8000/fr/`.

In either case, you can view the site in `/en/` or `/fr/` (no differences yet).

If this is all working as described, that means `i18n_patterns` and `LocaleMiddleware` are working!

# Step Three: Extend and add Wagtail Models

Before you start adding content and translating it, you'll need to add some models to Wagtail. Wagtail models are similar to [Django models](https://docs.djangoproject.com/en/4.1/topics/db/models/). One key difference is that Wagtail models handle views differently than Django models, but we'll go over that in a bit more detail when you add templates to your project. For right now, you mostly need to know that models provide the essential fields and structures for the content that will be stored in your database.

Many of the steps you'll be doing here have been borrowed from the [Getting Started tutorial](https://docs.wagtail.org/en/stable/getting_started/tutorial.html) for Wagtail.

## Extending the `HomePage` model

Right out of the box, Wagtail comes with a `home` app that provides a blank `HomePage` model. This model will define the home page of your website and what content appears on it. Go to the `home` directory in your project and open up `models.py` in your text editor or IDE. You'll see that all the model currently has in it by default is a `pass` command. So you're going to have to extend it to add content to your home page.

 Since this is a blog site, you should probably tell your readers what the blog is about and give them a reason to read it. All pages in Wagtail have a title by default, so you'll be able to add the blog title easily. So let's extend the `HomePage` model by adding text field for a blog summary to the model.

First, you'll need to add some additional import statements to the top of the page. This statement will import the `RichTextField` (one that let's you use bold, italics, and other formatting) from Wagtail:

```
from wagtail.fields import RichTextField
 ```

And this statement will import the panel you need to make sure your new field appears in the Wagtail admin as well:

```
from wagtail.admin.panels import FieldPanel
```

Once those import statements are added, delete `pass` from your `HomePage` model and replace it with:

```
summary = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
    ]

```

Your whole file should look like this right now:

```

from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    summary = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
    ]
```

Awesome! So what else do we need to have an attractive home page for the blog? An image is something most readers find appealing, so let's add an image to the `HomePage` model as well. Add the following code beneath your `summary` variable:

```
main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
```

And then add another line to `content_panels`:
```
FieldPanel('image'),
```

Your full `models.py` file should like like this now:

```
from dataclasses import Field
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    summary = RichTextField(blank=True)
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel('main_image'),
    ]

```

Now you have fields for a summary and for adding an image to your home page. To add those fields to the database, run the following migration commands:

```
python manage.py makemigrations
python manage.py migrate
```

You can run the development server if you like to check that the fields were successfully added to the admin panel. 

**NOTE:** Do not add any content just yet unless you don't mind losing it. It's fairly common to reset migrations early in developing a Django or Wagtail project.

To do that, run `python manage.py runserver` and then navigate to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin). Login with the credentials you created when you made your superuser. Then navigate to the Pages menu and click on Home. To edit the home page, click on the three little dots next to Home and click "Edit". You should see that your two fields have been added to the page.

## Adding blog models

Now that you've extended the Home page and added some useful fields, let's add the key parts of our blog. To do that, you'll need to create a new app with the command:

```
python manage.py startapp blog
```

Then you need to add that app to `INSTALLED_APPS` in `myblog/settings/base.py`:

```
INSTALLED_APPS = [
    "home",
    "search",
    # Insert this
    "blog",
    "wagtail_localize",
    "wagtail_localize.locales",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    # ...
]
```

#### A quick note on project structure
In Wagtail projects, it is generally a good idea to keep related models in separate apps because it makes it a little easier for you to manage changes that affect migrations. Also, it makes it a little easier to decide where to put new code or models. Some Wagtail developers like to use a "core" or "base" app for models that are used across their projects. Others prefer not to use that approach because it can make future migrations a little trickier to manage. Both approaches are valid! For this tutorial though, we're going to use the separate app approach.

Now that you have a blog app added to your project, navigate to `blog/models.py`. We're going to create two new page types for our blog. Wagtail is a CMS that uses a tree structure to organize content. There are parent pages and child pages. The ultimate parent page by default is the Home page. All other page types branch off of the Home page. Then child pages can branch off of those pages too.

First, you need to create a parent type for the blog. Most Wagtail developers will call these pages "index" pages, so this one will be called `BlogPageIndex`. Add the following code to your `models.py` file in the blog app:

```

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
```

This is a very simple version of `BlogIndexPage` with only a single `intro` field to describe the blog. You'll be adding a few more things to it later, but this will work right now for getting your blog set up.

Next, we need to create a child page called `BlogPage`. Think about the fields you need for a reader to enjoy a blog post. The title is included by default, so what else do you need? Blogs can get pretty messy without dates to organize them, so you'll need a `date` frield for sure. Let's type:

```
class BlogPage(Page):
    date = models.DateField("Post date")

    content_panels = Page.content_panels + [
        FieldPanel('date'),
    ]

```

Let's add an `intro` field to this page type too so that you can use it to give readers a preview of the blog post.

```
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
    ]
```

Note that `intro` has `max_length` added to it. This provides a character limit on the field so that writers won't get too long-winded and break your website's design with descriptions that are too long. You're welcome to give them more characters to work with if you want to.

You'll also need a `body` field to provide a place to put your post content (since creating a blog without a place to put content kind of defeats the purpose of a blog). 

```
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
```

## Making your blog searchable

Now, those fields are a good start for a basic blog. While we're here though, let's take a moment to make the content of your blog searchable. Update `models.py` with this code:

```
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
```

Then add `from wagtail.search import index` to your import statements so that the whole file looks like this:

```
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
```

Save all of your work. Then run `python manage.py makemigrations` and `python manage.py migrate` to check that the fields have been added to the Wagtail admin.

## Adding Wagtail StreamField

One of the best parts of Wagtail is [StreamField](https://docs.wagtail.org/en/stable/topics/streamfield.html). StreamField gives users the power to mix and match different "blocks" of content rather than having a strict structure for a page. For example, someone writing a blog post could add a "quote" block to highlight a particular quote or phrase from their post. Or they could add a "sidebar" block that includes a little extra bonus content on the page. There aren't many limits to the types of blocks you can create.

To show you StreamField in action, you're going to create a simple StreamField implementation in the blog post `body` using some of the [default blocks](https://docs.wagtail.org/en/stable/reference/streamfield/blocks.html?highlight=blocks) that come with Wagtail. First, add these import statements to your `models.py` file:

```
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
```


Next, replace the code in your `BlogPage` class with the following code:

```
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True)
```

Save your file and then run the migration commands `python manage.py makemigrations` and `python manage.py migrate`. Start up the development server real quick with `python manage.py runserver` then have a look at a blank Blog Page. You'll notice that the "body" section now has a row of blocks for you to choose from. You can experiment with combining blocks if you want to, but keep in mind that we are most likely going to reset our migrations at least once. So don't add any data you care about just yet.

## Adding custom models

One thing I always like to call a beginner's attention to is custom models. Because Wagtail is built on top of Django, it has the same quirks as Django does when it comes to custom models. In the Django documentation, it says "It’s highly recommended to set up a custom user model, even if the default User model is sufficient for you." This is because creating a custom user model in the middle of a project or with an existing database is a huge hassle. Even very smart people haven't figure out how to create a migration fix for it yet. The ticket to solve this issue has been open for _years_.

Anyway, I bring this up because Wagtail has some other models that are worth customizing before you go too far into a project so that you can save yourself some grief later on. Those models include the Wagtail `Image` model, the Wagtail `Documents` model, and the Wagtail `Renditions` model in addition to the `User` model. You may need them, you may not. But it's better to set them up now rather than set them up later.

Because we're using the separate app structure, we're going to put the `User` model in its own app, and we're going to put the other models in a `custom_media` app because they are all related to media. Type the following commands into your terminal:

```
python manage.py startapp custom_user
python manage.py startapp custom_media
```

Then update the code in your `INSTALLED_APPS` in `myblog/settings/base.py` to include the new apps:

```
INSTALLED_APPS = [
    "home",
    "search",
    "blog",
    "custom_media",
    "custom_user",
    "wagtail_localize",
]

```

### Custom media models

You should set up the custom media models first because those are more straightforward and won't cause issues with migrations. Navigate to `custom_media/models.py` and update your file so that it looks like this:

```
from django.db import models
from wagtail.documents.models import Document, AbstractDocument

from wagtail.images.models import Image, AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    # Add any extra fields to image here

    # To add a caption field:
    # caption = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        # 'caption',
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )

class CustomDocument(AbstractDocument):
    # Custom field example:
    # source = models.CharField(
    #     max_length=255,
    #     blank=True,
    #     null=True
    # )

    admin_form_fields = Document.admin_form_fields + (
        # Add all custom fields names to make them appear in the form:
    )
```

Let's take a closer look at some of the comments in the code here. You'll notice that there is an option to add a `caption` field to the image model. Wagtail doesn't include an image caption for `alt text` by default because the project is very focused on promoting good accessibility practices. Too often [captions fall short](), and the Wagtail maintainers are currently figuring out a better default way to support accessibility. In the meantime, the Wagtail project encourages you to set up accessbility practices that make the most sense for your particular project or organization.

Still, many projects need an image caption field for crediting photographers and artists. So the `CustomImage` model is the best place to do that. Feel free to uncomment the text to add a caption if you would like one. You can make similar change for the `CustomDocument` model too if there is any information that would be useful for you to keep track of with documents. You don't _have_ to add anything though. It's totally optional for completing the rest of this tutorial.


### Custom User model

Now, you might be wondering why I didn't have you go through the migration steps after adding those last few models. Welp, it's because we've been reaching the part of the tutorial I've been warning you about. After we add the `CustomUser` model, we're going to have to reset our migrations. Why? Let's find out together here.

First, navigate to `custom_user/models.py` and add the following code to your file and save it:

```
from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

```

Now save your code and run your first migration command, `python manage.py makemigrations`. You should get an error message that is similar to "Migration admin.0001_initial is applied before its dependency app.0001_initial on database 'default' ". Tables related to the `User` model in Django are some of the very first that are set up when you start a new project. So if you try to apply a custom version of the `User` model after the initial migration for your first app, you're going to get an error.

How do we fix this then? There are a few different appraoches you can take. Because your project is still in development though and you're currently using the default sqlite database for working on it, one of the easiest approaches for beginners to learn is to reset the migrations.

There are multiple approaches to resetting migrations too. But for this project, we're going to delete all our existing migration files along with the database then run our migration commands again. Here's how you do that.

1. Go to each `migrations` folder for the `blog` app (we'll go in alaphabetical order).
2. Delete all of the files in the folder except for `__init.py__`.
3. Open the `pycache` folder in the `migrations` folder and delete all of the files there as well.

Repeat this process for the `home` app and the `myblog` app. There shouldn't be any migration files in `custom_media` or `custom_user` yet but you can doublecheck that if you want. Next, find your database. It should have a name like `db.sqlite3`. Delete your database file as well.

Make sure one more time that all of your migration files have been removed. Then run your first migration command `python manage.py makemigrations` to create the new migrations you need. If you receive an error, delete all of the migration files and the database again. Be extra sure the you removed the `pycache` files in each app as well. If there is no error, then run `python manage.py migrate` to create fresh migrations in your database.

Since you deleted the database, you're going to have to create a new superuser to access the admin section of Wagtail again. So run `python manage.py createsuperuser` to create a new superuser. Then test it by running `python manage.py runserver` and navigating to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to log in.

Now you have a good foundation for customizing these critical models. You might not feel like this has added a lot to the project. But trust me, you'll be glad you took these steps further down the line. Next, we're going to add some additional models to our code called `snippets` along with some templates that will help our website look a little nicer.