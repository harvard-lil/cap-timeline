from django.contrib import admin
from django.urls import path, re_path
from research import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('data/events/', views.events),
    path('data/events/<int:event_id>', views.event),
    path('data/years/', views.years),
    path('data/groups/', views.groups),
    path('data/groups-by-region/', views.groups_by_region),
    path('data/year-settings/', views.year_settings),
    re_path(r'^.*/$', views.index)
]
