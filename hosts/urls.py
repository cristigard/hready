from django.urls import path
from .views import ( upload_view, CreateCityView, ListCityView,
                   UpdateCityView, DeleteCityView, ListReservationView, 
                   ListCommisionsMonthView,ListCommisionsByCityView )


urlpatterns = [
    path('upload/', upload_view, name='upload-view'),
    path('cities/', ListCityView.as_view(), name='list-cities'),
    path('add-city/', CreateCityView.as_view(), name='add-city'),
    path('update-city/<int:pk>/', UpdateCityView.as_view(), name='update-city'),
    path('delete-city/<int:pk>/', DeleteCityView.as_view(), name='delete-city'),
    path('reservations/', ListReservationView.as_view(), name='list-reservations'),
    path('month-commission/', ListCommisionsMonthView.as_view(), name='month-commission'),
    path('city-commission/', ListCommisionsByCityView.as_view(), name='city-commission'),
]
