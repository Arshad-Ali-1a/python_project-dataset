from django.urls import path
from . import views


app_name="sort_colleges"
urlpatterns = [
    path("", views.index, name="index"),
    path("display",views.display, name="display")
]
