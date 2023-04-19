# Generated by Django 4.1.3 on 2023-02-01 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('accountsApp', '0008_alter_customer_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to=utils.UploadFile.upload_to, verbose_name='تصویر پروفایل'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]