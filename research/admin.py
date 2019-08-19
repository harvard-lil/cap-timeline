from django.contrib import admin
from research.models import Event, KeyEvent, Finding, Weight, Image, Citation, Tag


admin.site.register(Event)
admin.site.register(KeyEvent)
admin.site.register(Finding)
admin.site.register(Weight)
admin.site.register(Image)
admin.site.register(Citation)
admin.site.register(Tag)
