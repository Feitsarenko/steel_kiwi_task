from easycart import BaseCart
from products.models import Product
from django.views.generic import TemplateView
from django.views.generic import View
from django.conf import settings
import stripe
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

stripe.api_key = settings.STRIPE_SECRET_KEY


class Cart(BaseCart):

    def get_queryset(self, pks):
        return Product.objects.filter(pk__in=pks)


class PageCart(TemplateView):
    template_name = 'carts/cart_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class StripeCharge(View):
    http_method_names = ('post',)

    def post(self, request):

        charge = stripe.Charge.create(
            amount=int(float(request.session['easycart']['totalPrice']))*100,
            currency='usd',
            description='A Django Charge',
            source=request.POST.get('stripeToken')
        )
        Cart(request).empty()
        return HttpResponseRedirect(reverse('cart'))

