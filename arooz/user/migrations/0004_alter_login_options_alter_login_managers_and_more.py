# Generated by Django 4.1.3 on 2022-12-14 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_headerflash_offer_product_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='login',
            options={},
        ),
        migrations.AlterModelManagers(
            name='login',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='login',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='login',
            name='email',
        ),
        migrations.RemoveField(
            model_name='login',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='login',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='login',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='login',
            name='is_customer',
        ),
        migrations.RemoveField(
            model_name='login',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='login',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='login',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='login',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='login',
            name='password',
        ),
        migrations.RemoveField(
            model_name='login',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='user.login'),
        ),
        migrations.AlterField(
            model_name='login',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
