from django import template

from navigation.models import FooterText, MainNavigation
from wagtail.models import Locale

register = template.Library()
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/

@register.inclusion_tag("navigation/footer.html", takes_context=True)
def get_footer_text(context):
    footer_text = ""
    if FooterText.objects.first() is not None:
        footer_text = FooterText.objects.first().localized.body

    return {
        "footer_text": footer_text,
    }

@register.inclusion_tag("navigation/main_navigation.html", takes_context=True)
def get_main_navigation(context):
    request = context["request"]
    locale = Locale.objects.get(language_code=request.LANGUAGE_CODE)
    menu_items = MainNavigation.objects.get(locale=locale)
        
    return {
        "menu_items": menu_items,
    }

