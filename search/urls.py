from django.urls import path, include
from . import views

app_name = "search"


urlpatterns = [
    path(
        "by_name/",
        views.SearchNameApiView.as_view(),
        name="search_name",
    ),
    path(
        "by_number/",
        views.SearchNumberApiView.as_view(),
        name="search_number",
    ),
]
