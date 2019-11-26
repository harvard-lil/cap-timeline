from django.contrib import admin
from research.models import Event, Finding, Weight, Image, Citation, Group, Relationship, Region


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date','end_date',  'description_short', 'type', 'id', 'hide', 'political_dissidents', 'weight']


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = ["title", "type", "publication_title"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "region"]



@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ["id", "preceding_event", "succeeding_event"]

admin.site.register(Finding)
admin.site.register(Weight)
admin.site.register(Image)
admin.site.register(Region)
