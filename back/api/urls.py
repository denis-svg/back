from django.urls import path

from . import views

urlpatterns = [
    path('events/', views.getEventHours),
    path('eventsby/', views.geteventsBy),
    path('persons/', views.personsCount),
    path('avgpersons/', views.personsAvg),
    path('urls/', views.urls),
]
