from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import (DjangoFilterBackend, FilterSet, DateTimeFromToRangeFilter,
                                           CharFilter)
from rest_framework.filters import OrderingFilter
from ..models import Employee, Team
from .serializers import EmployeeSerializer, TeamSerializer
from employee_management.paginations import PagePagination


class EmployeeFilter(FilterSet):
    """
    Filter set class for searching in employees.
    It can filter based on employee name(q) or create_date.
    """
    q = CharFilter(field_name='name', lookup_expr='icontains')
    create_date = DateTimeFromToRangeFilter()

    class Meta:
        model = Employee
        fields = ['q', 'name', 'employee_id', 'create_date']


class TeamFilter(FilterSet):
    """
    Filter set class for searching in teams.
    It can filter based on team name, create_date or update_date.
    """
    q = CharFilter(field_name='name', lookup_expr='icontains')
    create_date = DateTimeFromToRangeFilter()
    update_date = DateTimeFromToRangeFilter()

    class Meta:
        model = Team
        fields = ['name', 'create_date', 'update_date']


class EmployeeListCreateAPIView(ListCreateAPIView):
    """
       View class for listing, searching and creating employees.
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = EmployeeFilter
    ordering_fields = ['create_date', 'update_date']
    ordering = ['-create_date']
    serializer_class = EmployeeSerializer
    pagination_class = PagePagination
    queryset = Employee.objects.all()


class EmployeeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class TeamListCreateAPIView(ListCreateAPIView):
    """
       View class for listing, searching and creating teams.
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TeamFilter
    ordering_fields = ['create_date', 'update_date', 'name']
    ordering = ['-create_date']
    serializer_class = TeamSerializer
    pagination_class = PagePagination
    queryset = Team.objects.all()


class TeamRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
