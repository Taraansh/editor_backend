# Generated by Django 4.2.2 on 2023-07-03 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webpages', '0002_rename_owner_email_page_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='user_email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
