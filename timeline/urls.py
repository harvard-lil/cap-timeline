from django.contrib import admin
from django.urls import path

from research import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('events', views.events),
    path('events/<int:event_id>', views.event),
    path('years', views.years),
]
