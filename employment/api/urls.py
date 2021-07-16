from django.urls import path
from .views import EmployeeListCreateAPIView, EmployeeRetrieveUpdateDestroyAPIView, TeamListCreateAPIView, \
    TeamRetrieveUpdateDestroyAPIView, TeamEmployeeListCreateAPIView, TeamEmployeeRetrieveUpdateDestroyAPIView

app_name = 'employment-api'

urlpatterns = [
    path('employees/', EmployeeListCreateAPIView.as_view(), name="employee_list_create"),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyAPIView.as_view(),
         name="employee_retrieve_update_destroy"),

    path('teams/', TeamListCreateAPIView.as_view(), name="team_list_create"),
    path('teams/<int:pk>/', TeamRetrieveUpdateDestroyAPIView.as_view(),
         name="team_retrieve_update_destroy"),

    path('team-employees/', TeamEmployeeListCreateAPIView.as_view(), name="team_employee_list_create"),
    path('team-employees/<int:pk>/', TeamEmployeeRetrieveUpdateDestroyAPIView.as_view(),
         name="team_employee_retrieve_update_destroy"),
]
