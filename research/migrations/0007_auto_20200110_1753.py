# Generated by Django 2.2.8 on 2020-01-10 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0006_theme_timeline'),
    ]

    operations = [
        migrations.AddField(
            model_name='meta',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='meta',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]