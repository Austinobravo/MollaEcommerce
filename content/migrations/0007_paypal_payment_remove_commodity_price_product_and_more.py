# Generated by Django 4.1.2 on 2022-11-19 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0006_rename_payment_stripe_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paypal_Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paypal_charge_id', models.CharField(max_length=100)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='commodity_price',
            name='product',
        ),
        migrations.DeleteModel(
            name='Commodity',
        ),
        migrations.DeleteModel(
            name='Commodity_Price',
        ),
    ]