from django.urls import path
from .views import EmployeeListCreateAPIView, EmployeeRetrieveUpdateDestroyAPIView, TeamListCreateAPIView, \
    TeamRetrieveUpdateDestroyAPIView

app_name = 'employment-api'

urlpatterns = [
    path('employees/', EmployeeListCreateAPIView.as_view(), name="employee_list_create"),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyAPIView.as_view(),
         name="employee_retrieve_update_destroy"),

    path('teams/', TeamListCreateAPIView.as_view(), name="team_list_create"),
    path('teams/<int:pk>/', TeamRetrieveUpdateDestroyAPIView.as_view(),
         name="team_retrieve_update_destroy"),

]
