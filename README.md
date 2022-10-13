# Step Four: Add custom models

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

Let's take a closer look at some of the comments in the code here. You'll notice that there is an option to add a `caption` field to the image model. Wagtail doesn't include an image caption for `alt text` by default. Many projects need an image caption field for crediting photographers and artists. So the `CustomImage` model is the best place to do that. Feel free to uncomment the text to add a caption if you would like one. You can make similar change for the `CustomDocument` model too if there is any information that would be useful for you to keep track of with documents. You don't _have_ to add anything though. It's totally optional for completing the rest of this tutorial.

One thing that is not optional though is updating our image model references. First, you'll need to add the following settings to the bottom of your `base.py` settings file:

```
# Custom models

WAGTAILIMAGES_IMAGE_MODEL = 'custom_media.CustomImage'

WAGTAILDOCS_DOCUMENT_MODEL = 'custom_media.CustomDocument'

```


These settings tell Wagtail which custom models you're using. Even with those set though, you're going to have update some references in your code as well. Fortunately, you only need to make one update for this particular project. Navigate to `home/models.py`. Then add the following import statement to the top of your file:

```
from wagtail import images
```
Then update your `main_image` model so that it looks like this:

```
    main_image = models.ForeignKey(
        images.get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
```
What you're doing with this code is collecting the string for the name of your CustomImage model so that you can point Wagtail to your custom model instead of the default `wagtailimages` model.

### Custom User model

Now, you might be wondering why I didn't have you go through the migration steps after adding those last few models. Welp, it's because we've been reaching the part of the tutorial I've been warning you about. After we add the `CustomUser` model, we're going to have to reset our migrations. Why? Let's find out together here.

First, navigate to `custom_user/models.py` and add the following code to your file and save it:

```
from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```
Then navigate to your `base.py` file in settings and update the `Custom model` section to include the custom user model:

```
# Custom models

WAGTAILIMAGES_IMAGE_MODEL = 'custom_media.CustomImage'

WAGTAILDOCS_DOCUMENT_MODEL = 'custom_media.CustomDocument'

AUTH_USER_MODEL = 'custom_user.User'
```


Now save your code and run the migration commands `python manage.py makemigrations` and `python manage.py migrate`. You should get an error message that is similar to "Migration admin.0001_initial is applied before its dependency app.0001_initial on database 'default' ". Tables related to the `User` model in Django are some of the very first that are set up when you start a new project. So if you try to apply a custom version of the `User` model after the initial migration for your first app, you're going to get an error.

How do we fix this then? There are a few different appraoches you can take. Because your project is still in development though and you're currently using the default sqlite database for working on it, one of the easiest approaches for beginners to learn is to reset the migrations.

There are multiple approaches to resetting migrations too. But for this project, we're going to delete all our existing migration files along with the database then run our migration commands again. Here's how you do that.

1. Go to each `migrations` folder for the `blog` app (we'll go in alaphabetical order).
2. Delete all of the files in the folder except for `__init.py__`.
3. Open the `pycache` folder in the `migrations` folder and delete all of the files there as well.

Repeat this process for the `home` app. There shouldn't be any migration files in `custom_media` or `custom_user` yet but you can doublecheck that if you want. Next, find your database. It should have a name like `db.sqlite3`. Delete your database file as well.

Make sure one more time that all of your migration files have been removed. Then run your first migration command `python manage.py makemigrations` to create the new migrations you need. If you receive an error, delete all of the migration files and the database again. Be extra sure the you removed the `pycache` files in each app as well. If there is no error, then run `python manage.py migrate` to create fresh migrations in your database.

Since you deleted the database, you're going to have to create a new superuser to access the admin section of Wagtail again. So run `python manage.py createsuperuser` to create a new superuser. Then test it by running `python manage.py runserver` and navigating to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to log in.

Now you have a good foundation for customizing these critical models. You might not feel like this has added a lot to the project. But trust me, you'll be glad you took these steps further down the line. Next, we're going to add some additional models to our code called `snippets` along with some templates that will help our website look a little nicer.