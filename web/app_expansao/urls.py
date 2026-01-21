from django.urls import path

from .views import location_create

urlpatterns = [
    path("locations/new/", location_create, name="location_create"),
]
