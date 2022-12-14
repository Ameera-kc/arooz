# Generated by Django 4.1.3 on 2022-12-14 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableSizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=3)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.product')),
            ],
        ),
    ]
