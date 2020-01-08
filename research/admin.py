from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q

from research.models import Event, Finding, Weight, Image, \
    Citation, Group, Relationship, Region, Theme, Meta


class TimelineFilter(SimpleListFilter):
    title = 'timeline'
    parameter_name = 'timeline'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return [(timeline.slug, timeline.title) for timeline in Meta.objects.all()]

        timelines = request.user.timelines.all()
        return [(timeline.slug, timeline.title) for timeline in timelines]

    def queryset(self, request, queryset):
        if request.user.is_superuser:
            return queryset
        timelines = request.user.timelines.all()
        user_timeline_query = Q()
        for timeline in timelines:
            user_timeline_query.add(Q(timeline=timeline), Q.OR)
        return queryset.filter(user_timeline_query)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'description_short', 'type', 'id', 'hide', 'weight']
    list_filter = (TimelineFilter,)

    def get_field_queryset(self, db, db_field, request):
        """
        Only showing allowed options in admin editing panel
        """
        if db_field.name == "timeline":
            user_timeline_query = Q()
            for timeline in request.user.timelines.all():
                user_timeline_query.add(Q(slug=timeline.slug), Q.OR)
            return db_field.remote_field.model._default_manager.filter(user_timeline_query)

        return super().get_field_queryset(db, db_field, request)


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = ["title", "type", "publication_title"]
    list_filter = (TimelineFilter,)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "region"]
    list_filter = (TimelineFilter,)


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ["event_one", "event_two", "id"]


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ["slug", "id", "name"]
    list_filter = (TimelineFilter,)


@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
    list_display = ["slug", "title", "subtitle"]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_filter = (TimelineFilter,)

admin.site.register(Finding)
admin.site.register(Weight)
admin.site.register(Image)
