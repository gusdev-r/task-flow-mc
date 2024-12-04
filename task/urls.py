from django.urls import path
from . import views

urlpatterns = [
    path("task/", views.TaskListView.as_view(), name="task-list"),
    path("task/config/", views.TaskConfigList.as_view(), name="task-list-config"),
    path("tasks/", views.TaskListByStatusView.as_view(), name="task-list-by-status"),
    path("tasks/<str:task_id>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("task/create/", views.TaskCreateView.as_view(), name="task-create"),
    path(
        "task/update/<str:task_id>/",
        views.TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "task/delete/<str:task_id>/", views.TaskDeleteView.as_view(), name="task-delete"
    ),
    path(
        "task/config/delete/<str:task_id>/",
        views.TaskConfigDeleteView.as_view(),
        name="task-config-delete",
    ),
    path(
        "tasks/<str:task_id>/config/",
        views.TaskConfigCreateView.as_view(),
        name="task-config-create",
    ),
]
