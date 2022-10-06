# Step Six: Add translatable navigation

In this step, you're going to learn about Wagtail Snippets. Snippets are pieces of code that can be used in multiple places across a project but that aren't a part of the page tree. Some common uses for Snippets include author profiles, menus, and footer content. The nice thing about Wagtail is you can use `TranslatableMixin` to make your snippets translatable by Wagtail Localize.

## Add a navigation app

To follow the separate apps structure, you're going to create a new app for all of the pieces related to website navigation. To create the app, type the following command into your terminal:

```
python manage.py startapp navigation
```

You'll use this app to store the models related to your translatable navigation snippets as well as some template tags that we'll use to help display the correct text for each locale. Curious what template tags are? You'll find out soon.

## Add a translatable footer model

First, you're going to add a translatable footer to your project. Having a translatable footer is handy for a blog because different countries can have different requirements when it comes to the legal notices you have to include on your website. To create your translatable footer, open `navigation/models.py` and add these import statements:

```
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet
```

You'll need `RichTextField` to add text to your foot, `TranslatableMixin` to make it translatable, `FieldPanel` to add a panel to the admin interface, and `register_snippet` to add this model as a Snippet rather than a Wagtail page model. Here's how you will set up the Snippet:

```
@register_snippet
class FooterText(TranslatableMixin, models.Model):
    body = RichTextField()


    panels = [
        FieldPanel("body"),
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = "Footer text"
        unique_together = [
            ("translation_key", "locale"),
        ]

```

Let's look at the different pieces. In setting up the class, you're telling `FooterText` to call on `TranslatableMixin`and `models.Model`. In the next lines, you're telling Wagtail, the body of the footer will include one `RichTextField` and the field will be rendered in one panel labeled "body".

The next few lines are a little different from setting up `Page` models in Wagail. Unlike pages, which include titles by default, Snippets need to have names given to them. You can either set them up to be named by users in the admin interface or you can hard code a name like you just did here with `return "Footer text" `. You'll get to see an example of the other naming approach when we code the navigation menu.

Under `Meta`, `verbose_name_plural` provides a plural version of the Snippet label so that you can keep the grammar hawks at your workplace happy. The `unique_together` is required for `TranslatableMixin`. It ties key pieces of your models together in the database and helps keep your locales organized.

Once you've added these pieces, do your migrations steps to update the database:

```
python manage.py makemigrations
python manage.py migrate
```
Start up your website with `python manage.py runserver`. On the lefthand menu, you'll see now that you have a menu labeled "Snippets" now. Click on it and there will be an item labeled "Footer text". Click on it and you should be taken to a page with a button that says "Add Footer Text". Click the button and fill out the field to add your footer text. If you want to continue with the badger theme, you can add "Copyright 2022 Badgers Inc. All rights reserved." and then click "Save".

You'll be returned to the snippet menu and there will now be an item labeled "Footer text" added to the list. When you hover over that item, you should see three buttons. "Edit", "Delete", and "Translate". Go ahead and click on "Translate".

You'll see a translation workflow similar to the one you used previously for the pages. Let's go ahead and manually translate the footer to "Copyright 2022 Badgers Inc. Tous droits réservés" and save the changes.

## Create a template tag for the footer

Now that you have some footer content and translated footer content, you're going to need a way to pull that content into the correct templates and locales. You're going to accomplish that with a custom [template tag](https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/). Template tags are bits of code that process data provided by a model and organize it before you pull the data into a template.

Since the template tag is related to navigation, go ahead and add a new directory to the `navigation` app called `templatetags`. In the directory, add a blank `__init__.py` file and a file called `navigation_tags.py`. Open `navigation_tags.py`. Add these three import statements to the top of the file.

```
from django import template

from navigation.models import FooterText

register = template.Library()
```

You'll need `template` to set up the `register` variable needed for custom template tags. You'll also need the Snippet model that you're going to be manipulating, which is why you're importing `FooterText`.

After adding the import statements, add this code beneath them:

```
@register.inclusion_tag("navigation/footer.html", takes_context=True)
def get_footer_text(context):
    footer_text = ""
    if FooterText.objects.first() is not None:
        footer_text = FooterText.objects.first().localized.body

    return {
        "footer_text": footer_text,
    }
```
In this section, you're telling Wagtail that your tag is connected to the template found at `navigation/footer.html` (which you'll create in the next section) and that your template tag needs to access the current context of the model. 

In the definition of `get_footer_text`, you created an empty string variable for `footer_text`, then you used an `if` statement to check that a `FooterText` object exists. Because there is only one item for the footer text, `.first()` was used to collect that first object and `.localized` was used to select the footer text `.body` associated with the locale for the page that the footer appears on and store it in the `footer_text` variable.

## Create templates for the footer

With this logic in place, now you can create templates for pulling the data onto your page. First, navigate to `myblog/templates` and create a directory labeled `navigation`. Then create a file called `navigation` and add a file labeled `footer.html` to it. In `footer.html`, let's add some code to collect and display the contents of the `footer_text` variable.

```
{% load wagtailcore_tags %}

<div class="copyright">
    {{ footer_text|richtext }}
</div>
```

You'll notice that the `richtext` filter is being applied again. Just like for the pages, this is to make sure that all of the characters in the rich text field display properly.

Now that you have a bit of code to display the footer, you can use the template tag you created to add this bit of code to your `base.html` file. Go to `templates.html` and update the statement at the top of the file so that it says:

```
{% load static wagtailcore_tags wagtailuserbar navigation_tags %}
```
At the bottom of the file, add the template tag `{% get_footer_text %}` after the closing `</body>` tag and just above the closing `</html>` tag.

Save all of your changes. Start your website with `python manage.py runserver` if you don't have it running already. Navigate to your home page at [http://127.0.0.1:8000/en](http://127.0.0.1:8000/en) and confirm that your footer is displaying properly. Now navigate to [http://127.0.0.1:8000/fr](http://127.0.0.1:8000/fr) and you should see the same footer but in French.

## Add a model for a translatable navigation menu

The footer is a fairly simple element to translate, especially if you put all of the content in a single rich text field. Now you're going to add a translatable main navigation menu at the top of the page. 

To keep the amount of time needed for this tutorial maneagable, the approach you're going to use is a bit more manual. It relies on the content editor to add labels and URLs rather than collecting them programatically. If you have time later, you can upgrade the menu to one that automatically collects page titles and URLs. I'll provide some sample code in the resources at the end.

Now, let's add a model for the menu to `navigation/models.py`. You should already have all the import statements you need, so add the following code beneath your `FooterText` snippet:

```
@register_snippet
class MainNavigation (TranslatableMixin, models.Model):
    name = models.CharField(max_length=255)

    menu_text = models.CharField(max_length=255)
    menu_url = models.URLField()

    panels = [
        FieldPanel("name"),
        FieldPanel("menu_text"),
        FieldPanel("menu_url"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Main navigation"
        unique_together = [
            ("translation_key", "locale"),
        ]

```

This code is very similar to the code you used for the footer snippet. One difference you'll notice though is that there is a `name` field as well as a line to `return self.name` in a string. The reason this approach is used rather than hardcoding the name is that you're going to have multiple links in your menu navigation and you're going to need to be able to tell them apart in the admin. The other fields will be the `menu_text` and the `menu_url` so that you can add as many links to the navigation menu as you need and also include external links if you would like to use them.

## Add a template tag for the navigation menu

Just like for the footer, you're going to add a template tag for the main navigation menu. Only with this template tag, you're going to collect all of the items for the menu rather than the first one. Open `navigtation/templatetags/navigation_tags.py` and add the following code beneath the code for your footer template tag:

```
@register.inclusion_tag("navigation/main_navigation.html", takes_context=True)
def get_main_navigation(context):
    menu_items = []
    if MainNavigation.objects.all() is not None:
        menu_items = MainNavigation.objects.all()
        
    return {
        "menu_items": menu_items,
    }
```

You could narrow down the objects to `.localized` objects in the template tag here if you wanted to. But I want to demonstrate how you can select `.localized` objects in the template as well. So let's look at how to do that in the next section.

## Add a template for the navigation menu

Under `myblog/templates/navigation`, add a file called `main_navigation.html`. Then add this code to the file:

```
<div class = "navigation">
    <ul>
        {% for menu_item in menu_items %}
            {% if menu_item.localized %}
               <li><a href = "{{ menu_item.localized.menu_url }}"> {{ menu_item.localized.menu_text }}</a></li>
            {% endif %}
        {% endfor %}
    </ul>
</div>
```

With this code, you're using a `for` statement to sort through all of the items in the `menu_items` variable and then an `if` statement to determine which ones are `.localized` and associated with the locale of that particular page. Then you're using the `.menu_url` and `.menu_text` attributes for each item to create links for your navigation menu.

Now you need to add the template tag to `base.html`. Insert this code after the `<head>` section and before the `<body>` section:

```
<header>
    {% get_main_navigation %}
</header>
```

Save all of your changes if you haven't already and then run `python manage.py runserver`. Navigate to your home page at [http://127.0.0.1:8000/en](http://127.0.0.1:8000/en) and confirm that your menu is displaying properly. Now navigate to [http://127.0.0.1:8000/fr](http://127.0.0.1:8000/fr) and you should see the same menu displayed in French.

## Add a language switcher

One last item that is super handy on a website with multiple languages is a language switcher that can rotate through the different locales.

Add a file to `myblog/templates/navigation` called `switcher.html`. Then add these lines to the file:

```
{% load i18n wagtailcore_tags %}
{% if page %}
    {% for translation in page.get_translations.live %}
        {% get_language_info for translation.locale.language_code as lang %}
        <a href="{% pageurl translation %}" rel="alternate" hreflang="{{ lang.code }}">
            {{ lang.name_local }}
        </a>
    {% endfor %}
{% endif %}
```
This code uses a combination of the i18n features in Django and Wagtail's translation features to collect all of the available live translations with `{% for translation in page.get_translations.live %}` and then collects all of the available languages with `{% get_language_info for translation.locale.language_code as lang %}`.

The next lines create a URL for each one of the translations and connects them to the appropriate language for the page that is displaying. Because there are only two locales available in this tutorial, they will just toggle back and forth between English and French.