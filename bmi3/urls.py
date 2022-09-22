from django.urls import path
from . import views

app_name = 'bmi3'

urlpatterns = [
    path('', views.index, name='index'),
    path('course-handbook/', views.course_handbook),
    # path('practical/<int:practical_id>/', views.practical, name='practical'),
    path('calendar', views.calendar, name='calendar'),
    path('api', views.api, name='api'),
    path('textbooks', views.textbooks, name='textbooks'),
    path('team', views.team),
    path('download/<str:pdf>', views.download, name='download'),
]