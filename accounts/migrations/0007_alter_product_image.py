# Generated by Django 5.0.6 on 2024-06-27 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, height_field=200, null=True, upload_to='static/images/', width_field=200),
        ),
    ]
