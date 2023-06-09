# Generated by Django 4.1.3 on 2023-01-30 18:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productApp', '0006_alter_brand_image_name_alter_product_image_name_and_more'),
        ('accountsApp', '0002_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ درج')),
                ('update_date', models.DateField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('is_finaly', models.BooleanField(default=False, verbose_name='وضعیت سفارش')),
                ('order_code', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='کد تولیدی برای سفارش')),
                ('discount', models.IntegerField(blank=True, default=0, null=True, verbose_name='تخفیف روی فاکتور')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='accountsApp.customer', verbose_name='مشتری')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارشات',
                'db_table': 't_order',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1, verbose_name='تعداد')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_detail1', to='orderApp.order', verbose_name='سفارش')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_detail2', to='productApp.product', verbose_name='کالا')),
            ],
            options={
                'verbose_name': 'جزیئات سفارش',
                'verbose_name_plural': 'جزیئات سفارشات',
                'db_table': 't_orderdetails',
            },
        ),
    ]
