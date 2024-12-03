from django.urls import path
from . import views

urlpatterns = [
    path("user/", views.UsersListView.as_view(), name="user-list"),
    path("users/active/", views.UsersListActiveView.as_view(), name="user-list-active"),
    path("users/<str:user_id>/", views.UserDetailView.as_view(), name="user-detail"),
    path("user/create/", views.UsersCreateView.as_view(), name="user-create"),
    path(
        "user/update/<str:user_id>/",
        views.UsersUpdateView.as_view(),
        name="user-update",
    ),
    path(
        "user/delete/<str:user_id>/", views.UserDeleteView.as_view(), name="user-delete"
    ),
]
