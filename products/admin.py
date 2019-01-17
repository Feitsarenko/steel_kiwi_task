from django.contrib import admin
from .models import *
from .forms import ProductForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']


class ActiveUsersListFilter(admin.SimpleListFilter):
    title = 'active'
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Comment and rating'),
            ('comment', 'Comment'),
            ('rating', 'Rating'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'active':
            return User.objects.filter(comment__isnull=True, like__isnull=True)
        if self.value() == 'comment':
            return User.objects.filter(comment__isnull=True)
        if self.value() == 'rating':
            return User.objects.filter(like__isnull=True)


UserAdmin.list_filter = (ActiveUsersListFilter,)


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'category', 'price', 'in_top_list', 'created_at', 'static_out_top_list')
    search_fields = ['name']
    readonly_fields = ['created_at', 'modified_at']


class LikeAdmin(admin.ModelAdmin):
    list_display = ('product', 'created_at',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment)
admin.site.register(Like, LikeAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(PageLoadsLogbook)
