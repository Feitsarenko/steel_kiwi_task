from django.conf.urls import url
from django.urls import re_path, include, path
from .views import PageCart, StripeCharge

urlpatterns = [
    # This pattern must always be the last
    path('cart/', PageCart.as_view(), name='cart'),
    url('', include('easycart.urls')),
    path('charge/', StripeCharge.as_view(), name='charge')
]
