from django import template

from navigation.models import FooterText, MainNavigation
from wagtail.models import Locale

register = template.Library()
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/

def filter_nav_for_locale(cls, locale):
    menu_items = None

    try:
        menu_items = cls.objects.filter(locale=locale)
    except cls.DoesNotExist:
        pass

    if not menu_items:
        try:
            menu_items = cls.objects.filter(locale=default_language())
        except cls.DoesNotExist:
            pass

    return menu_items

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
    print(locale)
    menu_items = filter_nav_for_locale(MainNavigation, locale)
        
    return {
        "menu_items": list(menu_items),
    }