from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet

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