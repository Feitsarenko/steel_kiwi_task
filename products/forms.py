from django import forms
from .models import Comment, Product
from tinymce.widgets import TinyMCE


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text', ]


class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(mce_attrs={'cols': 160, 'rows': 30}))

    class Meta:
        model = Product
        fields = ['category', 'description', 'name', 'image', 'price', 'slug', 'in_top_list', 'grade',\
                  'static_out_top_list', ]

