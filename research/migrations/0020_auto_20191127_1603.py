# Generated by Django 2.2.4 on 2019-11-27 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0019_auto_20191127_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=800)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='political_dissidents',
        ),
        migrations.AddField(
            model_name='event',
            name='themes',
            field=models.ManyToManyField(blank=True, related_name='events', to='research.Theme'),
        ),
    ]