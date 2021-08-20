# Generated by Django 3.2 on 2021-08-20 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlineshop', '0003_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='orderaddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=100)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='onlineshop.orderplaced')),
            ],
        ),
    ]
