from django.contrib import admin
from research.models import Event, Finding, Weight, Image, Citation, Tag, Relationship


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'type', 'id', 'hide']


admin.site.register(Finding)
admin.site.register(Relationship)
admin.site.register(Weight)
admin.site.register(Image)
admin.site.register(Citation)
admin.site.register(Tag)
