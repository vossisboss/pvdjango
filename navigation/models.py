from typing_extensions import Required
from django.db import models

from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, TranslatableMixin
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
    # menu_url = StreamField([
    #     ('menu_url', blocks.StructBlock([
    #         ('page', blocks.PageChooserBlock(required = False)),
    #         ('external_url', blocks.URLBlock(required = False)),
    #     ])),
    # ], null = True, use_json_field=True)

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