from django import template

register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(product, kart):
    keys = kart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False;


@register.filter(name='cart_quantity')
def cart_quantity(product, kart):
    keys = kart.keys()
    for id in keys:
        if int(id) == product.id:
            return kart.get(id)
    return 0;


@register.filter(name='price_total')
def price_total(product, kart):
    return product.price * cart_quantity(product, kart)


@register.filter(name='total_cart_price')
def total_cart_price(products, kart):
    sum = 0;
    for p in products:
        sum += price_total(p, kart)

    return sum
