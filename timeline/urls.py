from django.contrib import admin
from django.urls import path, re_path
from django.views.generic.base import TemplateView
from research import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/events/', views.events),
    path('data/events/<int:event_id>', views.event),
    path('data/years/', views.years),
    path('data/groups/', views.groups),
    path('data/groups-by-region/', views.groups_by_region),
    path('data/year-settings/', views.year_settings),
    path('', views.index),
    re_path(r'^.*$', views.index),
]
