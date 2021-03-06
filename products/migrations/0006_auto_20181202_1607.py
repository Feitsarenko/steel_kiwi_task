# Generated by Django 2.1.3 on 2018-12-02 16:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_auto_20181127_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='grade',
            field=models.CharField(choices=[('B', 'Base'), ('S', 'Standard'), ('P', 'Premium')], default='S', max_length=1),
        ),
        migrations.RemoveField(
            model_name='like',
            name='like',
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('product', 'user'), ('product', 'user_ip')},
        ),
    ]
