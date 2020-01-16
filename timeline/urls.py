from django.contrib import admin
from django.urls import path, re_path
from research import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('data/metas/', views.metas, name='get-metas'),
    path('data/<str:slug>/events/', views.events),
    path('data/<str:slug>/event-types/', views.event_types),
    path('data/<str:slug>/events/<int:event_id>', views.event),
    path('data/<str:slug>/years/', views.years, name='get-years'),
    path('data/<str:slug>/groups/', views.groups),
    path('data/<str:slug>/groups-by-region/', views.groups_by_region),
    path('data/<str:slug>/year-settings/', views.year_settings),
    path('data/<str:slug>/themes/', views.themes),
    path('data/<str:slug>/meta/', views.meta),
    re_path(r'^.*/$', views.index)
]
