# Generated by Django 5.1.3 on 2024-12-10 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_storestackuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storestackuser',
            name='user_type',
            field=models.CharField(choices=[('buyer', 'Buyer'), ('seller', 'Seller')], max_length=10, null=True),
        ),
    ]