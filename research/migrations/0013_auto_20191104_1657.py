# Generated by Django 2.2.4 on 2019-11-04 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0012_group_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citation',
            old_name='cite',
            new_name='caselaw_citation',
        ),
        migrations.RenameField(
            model_name='citation',
            old_name='book_or_article',
            new_name='publication_title',
        ),
        migrations.RenameField(
            model_name='citation',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='citation',
            name='author_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='citation',
            name='issue_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='citation',
            name='publication_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='citation',
            name='volume_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
