from django.contrib import admin
from research.models import Event, Finding, Weight, Image, Citation, Group, Relationship


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'type', 'id', 'hide', 'weight']


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = ["title", "type", "publication_title"]

admin.site.register(Finding)
admin.site.register(Relationship)
admin.site.register(Weight)
admin.site.register(Image)
admin.site.register(Group)
