import json
import requests
import markdown
from django.db import models
from timeline.settings import PERMA_KEY, PERMA_FOLDER, STORAGES, CAP_KEY, CAP_URL
from django.db.models import Q

class Region(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)

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

                url = CAP_URL + '?cite=' + self.caselaw_citation
                response = requests.get(
                    url,
                    headers={'Authorization': 'Token %s' % CAP_KEY}
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


class Relationship(models.Model):
    preceding_event = models.ForeignKey('Event', on_delete=models.DO_NOTHING, related_name='heads')
    succeeding_event = models.ForeignKey('Event', on_delete=models.DO_NOTHING, related_name='tails')
    description = models.TextField(blank=True)

    def __str__(self):
        return "%s is directly related to %s" % (self.succeeding_event.name, self.preceding_event.name,)


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
    hide = models.BooleanField(default=False)
    type = models.CharField(blank=True, null=True, max_length=100,
                            choices=(("us", "us"),
                                     ("world", "world"),
                                     ("legislation", "legislation"),
                                     ("caselaw", "caselaw")))

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
        for relationship in Relationship.objects.filter(Q(preceding_event__id=self.id) | Q(succeeding_event__id=self.id)):
            rel = relationship.succeeding_event if relationship.preceding_event.id == self.id else relationship.preceding_event
            relationships.append([rel.id, rel.type])

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
    data = models.FileField(storage=STORAGES['image_storage'])
    src = models.ForeignKey('Citation', null=True, related_name='images', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "%s %s" % (str(self.id), str(self.src.title))

    def save(self, *args, **kwargs):
        self.src.type = 'image'
        return super(Image, self).save(*args, **kwargs)
