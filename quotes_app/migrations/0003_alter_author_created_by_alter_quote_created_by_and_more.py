# Generated by Django 5.0 on 2023-12-29 18:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quotes_app", "0002_author_created_by_quote_created_by_tag_created_by"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="quote",
            name="created_by",
            field=models.IntegerField(verbose_name="created by user id"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="created_by",
            field=models.IntegerField(verbose_name="created by user id"),
        ),
    ]
