from django.db import models

from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
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



# @register_snippet
# class MainNavigation (TranslatableMixin, models.Model):
#     name = models.CharField(max_length=255)
#     page = blocks.PageChooserBlock(label="Page", required=False)
#     cta_url = blocks.URLBlock(label="URL", required=False)

#     panels = [
#         FieldPanel("body"),
#     ]

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Main navigation"

# @register_snippet
# class MainMenu(ClusterableModel):

#     name = models.CharField(max_length=255)
#     menu_sections = StreamField(
#         [("menu_section", MainMenuSectionBlock())],
#     )

#     panels = [
#         FieldPanel("name"),
#         StreamFieldPanel("menu_sections", classname="collapsible"),
#     ]

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Main menu"