# Generated by Django 4.1.3 on 2023-02-25 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('productApp', '0019_alter_brand_image_name_alter_product_image_name_and_more'),
        ('comments_scoring_whislistApp', '0002_alter_comment_is_active_scoring'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج محصول مورد علاقه')),
                ('favorite_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_user', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_product', to='productApp.product', verbose_name='محصول مورد علاقه')),
            ],
            options={
                'verbose_name': 'علاقه',
                'verbose_name_plural': 'علاقه مندی ها',
                'db_table': 't_favorite',
            },
        ),
    ]
