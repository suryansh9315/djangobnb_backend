from django.urls import path
from .views import PropertiesListView, CreateProperty, PropertiesDetailView, BookProperty, ReservationsListView, UserReservationsListView, ToggleFavourite

urlpatterns = [
    path('', PropertiesListView.as_view()),
    path('create', CreateProperty.as_view()),
    path('<uuid:pk>/', PropertiesDetailView.as_view()),
    path('<uuid:pk>/book', BookProperty.as_view()),
    path('<uuid:pk>/reservations', ReservationsListView.as_view()),
    path('myreservations/', UserReservationsListView.as_view()),
    path('<uuid:pk>/toogle_favourite', ToggleFavourite.as_view())
]