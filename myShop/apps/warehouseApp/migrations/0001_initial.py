# Generated by Django 4.1.3 on 2023-02-21 19:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('productApp', '0015_alter_brand_image_name_alter_product_image_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarehouseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warehouse_type_title', models.CharField(max_length=50, verbose_name='نوع انبار')),
            ],
            options={
                'verbose_name': 'نوع انبار',
                'verbose_name_plural': 'نوع انبار ها',
                'db_table': 't_warehouse_type',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(verbose_name='تعداد')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='قیمت')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_product', to='productApp.product', verbose_name='محصول')),
                ('user_registered', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_user_registered', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ثبت کننده')),
                ('warehouse_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse', to='warehouseApp.warehousetype', verbose_name='انبار')),
            ],
            options={
                'verbose_name': 'انبار',
                'verbose_name_plural': 'انبار ها',
                'db_table': 't_warehouse',
            },
        ),
    ]
