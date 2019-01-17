from django.urls import re_path
from .views import CategoryPageView, CategoryListView, ProductDetailsView, LikeView, MainView, ProductChooseWeekView


urlpatterns = [
    re_path(r'^product/$', CategoryListView.as_view(), name='category_list'),
    re_path(r'^main/$', MainView.as_view(), name='main_page'),
    re_path(r'^product/(?P<category_slug>[\w-]+)/$', CategoryPageView.as_view(), name='category_page'),
    re_path(r'^product/(?P<category_slug>[\w-]+)/(?P<product_slug>[\w-]+)$', ProductDetailsView.as_view(),
            name='product_details'),
    re_path(r'^product/(?P<category_slug>[\w-]+)/(?P<product_slug>[\w-]+)/like/$', LikeView.as_view(),
            name='like'),
    re_path(r'^choice_week/$', ProductChooseWeekView.as_view(), name='choice_week'),
]
