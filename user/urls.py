from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.GlobalContactViewSet)
app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path(
        "me/",
        views.UpdateUserView.as_view(
            {"get": "retrieve", "patch": "update", "put": "update"}
        ),
        name="update_user",
    ),
    path("add_contact/", views.AddContactView.as_view(), name="add_contact"),
    path("contacts/", include(router.urls)),
    path("mark_spam/<str:number>/", views.MarkSpamApiView.as_view(), name="mark_spam"),
]
