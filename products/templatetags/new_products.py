from django.template import Library
from products.models import Product

register = Library()


@register.inclusion_tag('product/new_product.html', name='new_products')
def list_new_product():
    products = Product.objects.order_by('category', '-created_at').distinct('category')
    return {'products': products}
