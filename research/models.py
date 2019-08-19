from django.db import models
# from django.contrib.postgres.fields import ArrayField


class Event(models.Model):
    name = models.CharField(max_length=1000)
    date = models.DateTimeField(null=True, blank=True)
    citation = models.ForeignKey('Citation', null=True, related_name='events', on_delete=models.DO_NOTHING)
    weight = models.ForeignKey('Weight', null=True, related_name='events', on_delete=models.DO_NOTHING)
    image = models.ForeignKey('Image', null=True, related_name='events', on_delete=models.DO_NOTHING)
    description_long = models.TextField(blank=True)
    description_short = models.CharField(max_length=800, blank=True)
    # tags = models.ArrayField()


class KeyEvent(models.Model):
    name = models.CharField(max_length=1000)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    description_long = models.TextField(blank=True)
    description_short = models.CharField(max_length=800, blank=True)

    def __str__(self):
        return self.name


class Finding(models.Model):
    description_short = models.CharField(max_length=1000, blank=True)
    description_long = models.TextField(blank=True)


class Weight(models.Model):
    level = models.PositiveIntegerField(null=True)
    description = models.CharField(blank=True, max_length=1000)


class Image(models.Model):
    data = models.FileField()
    src = models.ForeignKey('Citation', null=True, related_name='images', on_delete=models.DO_NOTHING)


class Citation(models.Model):
    name = models.CharField(max_length=800)
    url = models.URLField(blank=True, null=True)
    book_or_article = models.CharField(blank=True, null=True, max_length=2000)
    archived = models.URLField(blank=True, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)

