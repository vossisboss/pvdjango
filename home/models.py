from dataclasses import Field
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail import images


class HomePage(Page):
    summary = RichTextField(blank=True)
    main_image = models.ForeignKey(
        images.get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel('main_image'),
    ]