# Generated by Django 2.2.16 on 2022-12-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_auto_20221202_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(verbose_name='Количество'),
        ),
    ]
