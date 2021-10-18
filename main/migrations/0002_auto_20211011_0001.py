# Generated by Django 3.2.7 on 2021-10-10 18:31

import colorfield.fields
import django.core.validators
from django.db import migrations, models

import main.models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="year",
            name="colourback",
            field=colorfield.fields.ColorField(
                blank=True,
                default="rgb(73, 109, 137)",
                max_length=18,
                null=True,
                verbose_name="colourback",
            ),
        ),
        migrations.AlterField(
            model_name="year",
            name="colourtext",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#FFF00C",
                max_length=18,
                null=True,
                verbose_name="colourtext",
            ),
        ),
        migrations.AlterField(
            model_name="year",
            name="year",
            field=models.IntegerField(
                blank=True,
                null=True,
                unique=True,
                validators=[
                    django.core.validators.MinValueValidator(2003),
                    main.models.max_value_current_year,
                ],
                verbose_name="Year",
            ),
        ),
    ]
