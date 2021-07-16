from django.urls import path
from .views import EmployeeListCreateAPIView, PropertyRetrieveUpdateDestroyAPIView

app_name = 'employment-api'

urlpatterns = [
    path('employees/', EmployeeListCreateAPIView.as_view(), name="list_create"),
    path('employees/<int:pk>/', PropertyRetrieveUpdateDestroyAPIView.as_view(),
         name="retrieve_update_destroy"),

]
