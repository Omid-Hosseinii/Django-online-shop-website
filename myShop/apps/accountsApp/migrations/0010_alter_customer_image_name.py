# Generated by Django 4.1.3 on 2023-02-07 16:24

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('accountsApp', '0009_alter_customer_image_name_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to=utils.UploadFile.upload_to, verbose_name='تصویر پروفایل'),
        ),
    ]