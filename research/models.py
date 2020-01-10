import json
import requests
import markdown

from autoslug import AutoSlugField
from django.db import models
from django.db.models import Q
from django.conf import settings


class Region(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    timeline = models.ForeignKey('Meta', null=True, blank=True, related_name='regions', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    def as_json(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower()
            self.slug = self.slug.replace(' ', '_')

        super(Region, self).save(*args, **kwargs)


class Group(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    region = models.ForeignKey('Region', blank=True, null=True, on_delete=models.DO_NOTHING)
    timeline = models.ForeignKey('Meta', null=True, blank=True, related_name='groups', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    def as_json(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower()
            self.slug = self.slug.replace(' ', '_')

        super(Group, self).save(*args, **kwargs)


class Citation(models.Model):
    title = models.CharField(max_length=800)
    caselaw_citation = models.CharField(max_length=800, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    publication_title = models.CharField(blank=True, null=True, max_length=2000)
    author_name = models.CharField(blank=True, null=True, max_length=1000)
    volume_number = models.IntegerField(blank=True, null=True)
    issue_number = models.IntegerField(blank=True, null=True)
    archived_url = models.URLField(blank=True, null=True)
    archived_date = models.DateTimeField(blank=True, null=True)
    publication_date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=100, blank=True, null=True,
                            choices=(("image", "image"),
                                     ("caselaw", "caselaw"),
                                     ("webpage", "webpage"),
                                     ("article", "article"),
                                     ("book", "book")))
    timeline = models.ForeignKey('Meta', null=True, blank=True, related_name='citations', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

    def as_json(self):
        return dict(
            title=self.title,
            cite=self.caselaw_citation,
            url=self.url,
            publication_title=self.publication_title,
            archived_url=self.archived_url,
            archived_date=str(self.archived_date),
            type=self.type
        )

    def save(self, *args, **kwargs):
        if self.caselaw_citation:
            if not self.url:
                # find case

                url = settings.CAP_URL + '?cite=' + self.caselaw_citation
                response = requests.get(
                    url,
                    headers={'Authorization': 'Token %s' % settings.CAP_KEY}
                )
                resp = response.json()
                if resp['count'] == 1:
                    case = resp['results'][0]
                    self.title = case['name_abbreviation']
                    self.url = case['frontend_url']
                    self.type = 'caselaw'
                    self.volume_number = case['volume']['volume_number']
                    self.publication_date = case['decision_date']
                    self.publication_title = 'Caselaw Access Project'

        if self.url and not self.archived_url:
            if settings.PERMA_KEY:
                data = {"url": self.url, "folder": settings.PERMA_FOLDER}
                res = requests.post("https://api.perma.cc/v1/archives/?api_key=%s" % settings.PERMA_KEY,
                                    data=json.dumps(data),
                                    headers={'Content-type': 'application/json'},
                                    allow_redirects=True)

                if res.status_code == 201:
                    content = json.loads(res.content.decode())
                    self.archived_url = "https://perma.cc/%s" % content['guid']
                    self.archived_date = content['creation_timestamp']

        return super(Citation, self).save(*args, **kwargs)


class Relationship(models.Model):
    event_one = models.ForeignKey('Event', on_delete=models.DO_NOTHING, related_name='heads')
    event_two = models.ForeignKey('Event', on_delete=models.DO_NOTHING, related_name='tails')
    description = models.TextField(blank=True)

    def __str__(self):
        return "%s is directly related to %s" % (self.event_one.name, self.event_two.name,)


class Theme(models.Model):
    name = models.CharField(max_length=800)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    timeline = models.ForeignKey('Meta', null=True, blank=True, related_name='themes', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower()
            self.slug = self.slug.replace(' ', '_')

        super(Theme, self).save(*args, **kwargs)


class Event(models.Model):
    name = models.CharField(max_length=1000)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    citation = models.ManyToManyField(Citation, blank=True, related_name='events')
    weight = models.ForeignKey('Weight', null=True, blank=True, related_name='events', on_delete=models.DO_NOTHING)
    image = models.ForeignKey('Image', null=True, blank=True, related_name='events', on_delete=models.DO_NOTHING)
    description_long = models.TextField(blank=True)
    description_short = models.CharField(max_length=800, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    themes = models.ManyToManyField(Theme, blank=True, related_name='events')
    hide = models.BooleanField(default=False)
    type = models.CharField(blank=True, null=True, max_length=100,
                            choices=(("us", "us"),
                                     ("world", "world"),
                                     ("legislation", "legislation"),
                                     ("caselaw", "caselaw"),
                                     ("administrative", "administrative")))
    timeline = models.ForeignKey('Meta', null=False, blank=False, related_name='events', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    def as_json(self):
        citations = []
        for cite in self.citation.all():
            c = cite.as_json() if self.citation else None
            if c:
                citations.append(c)

        start_date = str(self.start_date)
        start_date_parsed = self.start_date.strftime("%b %d, %Y") if self.start_date else None

        end_date = str(self.end_date) if self.end_date else None
        end_date_parsed = self.end_date.strftime("%b %d, %Y") if self.end_date else None

        relationships = []
        for relationship in Relationship.objects.filter(
                Q(event_one__id=self.id) | Q(event_two__id=self.id)):
            rel = relationship.event_two if relationship.event_one.id == self.id else relationship.event_one
            relationships.append([rel.id, rel.type])

        themes = {}
        for theme in self.themes.all():
            themes[theme.slug] = theme.name

        return dict(
            id=self.id,
            name=self.name,
            start_date=start_date,
            start_date_parsed=start_date_parsed,
            end_date=end_date,
            end_date_parsed=end_date_parsed,
            citations=citations,
            type=self.type,
            hide=self.hide,
            themes=themes,
            relationships=relationships,
            description_long=markdown.markdown(self.description_long),
            description_short=markdown.markdown(self.description_short),
            groups=[group.as_json() for group in self.groups.all()],
        )


class Finding(models.Model):
    """
        Editorializing events
    """
    description_short = models.CharField(max_length=1000, blank=True)
    description_long = models.TextField(blank=True)
    events = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return self.description_short


class Weight(models.Model):
    level = models.PositiveIntegerField(null=True)
    description = models.CharField(blank=True, max_length=1000)

    def __str__(self):
        return "%s: %s" % (self.level, self.description)


class Image(models.Model):
    data = models.FileField(storage=settings.STORAGES['image_storage'])
    src = models.ForeignKey('Citation', null=True, related_name='images', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "%s %s" % (str(self.id), str(self.src.title))

    def save(self, *args, **kwargs):
        self.src.type = 'image'
        return super(Image, self).save(*args, **kwargs)


class Meta(models.Model):
    title = models.CharField(null=False, blank=False, max_length=1000)
    subtitle = models.TextField(null=True, blank=True)
    slug = AutoSlugField(max_length=255, populate_from="title", unique=True, null=False, blank=False, primary_key=True)

    def __str__(self):
        return self.title

    def as_json(self):
        return dict(
            title=self.title,
            subtitle=self.subtitle,
            slug=self.slug,
        )

    def publish(self):
        import subprocess
        subprocess.call(["fab", "create_json:timeline=%s" % self.slug])
        subprocess.call(["fab", "create_meta:timeline=%s" % self.slug])

    @classmethod
    def publish_all_metas(cls):
        import subprocess
        subprocess.call(["fab", "create_meta"])
