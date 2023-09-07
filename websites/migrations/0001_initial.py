# Generated by Django 3.1 on 2020-12-16 19:22

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Website",
            fields=[
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("url_path", models.CharField(max_length=512, unique=True)),
                ("title", models.CharField(max_length=512, blank=True, null=True)),
                ("publish_date", models.DateTimeField(blank=True, null=True)),
                ("type", models.CharField(default="course", max_length=24)),
                ("metadata", models.JSONField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="WebsiteContent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4)),
                ("title", models.CharField(max_length=512, blank=True, null=True)),
                ("type", models.CharField(max_length=24, blank=True, null=True)),
                ("markdown", models.TextField(blank=True, null=True)),
                ("metadata", models.JSONField(blank=True, null=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contents",
                        to="websites.websitecontent",
                    ),
                ),
                (
                    "website",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="websites.website",
                    ),
                ),
            ],
            options={
                "unique_together": {("website", "uuid")},
            },
        ),
    ]
