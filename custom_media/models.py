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



