from django import template
  
register = template.Library()
  


@register.filter()
def get_space(mapping,value):

    if not mapping: return None
    return mapping.get(value)