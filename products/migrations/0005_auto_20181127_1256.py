# Generated by Django 2.1.3 on 2018-11-27 12:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='like',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
