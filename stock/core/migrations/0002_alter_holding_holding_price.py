# Generated by Django 4.1.2 on 2022-11-02 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holding',
            name='holding_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]