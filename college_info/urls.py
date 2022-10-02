from django.urls import path
from . import views

app_name="college_info"

urlpatterns = [
    # path("",views.index,name="index"),
    path("<str:college>", views.index, name="index"),
]
