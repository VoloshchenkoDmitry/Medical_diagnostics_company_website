from django.urls import path

from . import views

app_name = "appointments"

urlpatterns = [
    path("", views.AppointmentListView.as_view(), name="list"),
    path(
        "create/<slug:service_slug>/",
        views.AppointmentCreateView.as_view(),
        name="create",
    ),  # Убедитесь, что есть этот путь
    path("<int:pk>/", views.AppointmentDetailView.as_view(), name="detail"),
    path("<int:pk>/cancel/", views.AppointmentCancelView.as_view(), name="cancel"),
    path(
        "api/available-slots/<slug:service_slug>/",
        views.AvailableTimeSlotsView.as_view(),
        name="available_slots",
    ),
]
