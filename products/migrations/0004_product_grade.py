# Generated by Django 2.1.3 on 2018-11-20 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='grade',
            field=models.CharField(choices=[('B', 'Base'), ('S', 'Standard'), ('P', 'Premium')], default='S', max_length=1),
        ),
    ]
