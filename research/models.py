import json
import requests
from django.db import models

from timeline.settings import PERMA_KEY, PERMA_FOLDER


class Tag(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=1000)
    date = models.DateTimeField(null=True, blank=True)
    citation = models.ForeignKey('Citation', null=True, blank=True, related_name='events', on_delete=models.DO_NOTHING)
    weight = models.ForeignKey('Weight', null=True, blank=True, related_name='events', on_delete=models.DO_NOTHING)
    image = models.ForeignKey('Image', null=True, blank=True, related_name='events', on_delete=models.DO_NOTHING)
    description_long = models.TextField(blank=True)
    description_short = models.CharField(max_length=800, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.description_short


class Weight(models.Model):
    level = models.PositiveIntegerField(null=True)
    description = models.CharField(blank=True, max_length=1000)

    def __str__(self):
        return "%s: %s" % (self.level, self.description)


class Image(models.Model):
    data = models.FileField()
    src = models.ForeignKey('Citation', null=True, related_name='images', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "%s %s" % (str(self.id), str(self.src.name))


class Citation(models.Model):
    name = models.CharField(max_length=800)
    url = models.URLField(blank=True, null=True)
    book_or_article = models.CharField(blank=True, null=True, max_length=2000)
    archived_url = models.URLField(blank=True, null=True)
    archived_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.url and not self.archived_url:
            if PERMA_KEY:
                data = {"url": self.url, "folder": PERMA_FOLDER}
                res = requests.post("https://api.perma.cc/v1/archives/?api_key=%s" % PERMA_KEY,
                                    data=json.dumps(data),
                                    headers={'Content-type': 'application/json'},
                                    allow_redirects=True)

                if res.status_code == 201:
                    content = json.loads(res.content.decode())
                    self.archived_url = "https://perma.cc/%s" % content['guid']
                    self.archived_date = content['creation_timestamp']

        return super(Citation, self).save(*args, **kwargs)
