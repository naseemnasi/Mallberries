from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product  , kart):
    keys = kart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False;

