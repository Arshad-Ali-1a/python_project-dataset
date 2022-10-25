from django.urls import path
from . import views

app_name="college_info"

urlpatterns = [
    # path("",views.index,name="index"),
    path("sections/<str:section>/<str:college_code>",views.sections,name="sections"),
    path("<str:college>", views.index, name="index"),
]
