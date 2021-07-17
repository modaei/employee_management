from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import (DjangoFilterBackend, FilterSet, DateTimeFromToRangeFilter,
                                           CharFilter, NumberFilter)
from rest_framework.filters import OrderingFilter
from ..models import Employee, Team, TeamEmployee
from .serializers import EmployeeSerializer, TeamSerializer, TeamEmployeeSerializer
from employee_management.paginations import PagePagination
from rest_framework.response import Response
from rest_framework import status


class EmployeeFilter(FilterSet):
    """
    Filter set class for searching in employees.
    It can filter based on employee name or create_date.
    """
    name = CharFilter(field_name='name', lookup_expr='icontains')
    create_date = DateTimeFromToRangeFilter()

    class Meta:
        model = Employee
        fields = ['name', 'employee_id', 'create_date']


class TeamFilter(FilterSet):
    """
    Filter set class for searching in teams.
    It can filter based on team name, create_date or update_date.
    """
    name = CharFilter(field_name='name', lookup_expr='icontains')
    create_date = DateTimeFromToRangeFilter()

    class Meta:
        model = Team
        fields = ['name', 'create_date']


class TeamEmployeeFilter(FilterSet):
    """
    Filter set class for searching in TeamEmployee.
    It can filter based on team_id, employee_id.
    """
    team = NumberFilter(field_name='team_id')
    employee = NumberFilter(field_name='employee_id')

    class Meta:
        model = TeamEmployee
        fields = ['team', 'employee']


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


class TeamEmployeeListCreateAPIView(ListCreateAPIView):
    """
     View class for listing, searching and creating TeamEmployee objects.
    """
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeamEmployeeFilter
    serializer_class = TeamEmployeeSerializer
    queryset = TeamEmployee.objects.all()


class TeamEmployeeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TeamEmployeeSerializer
    queryset = TeamEmployee.objects.all()

    def destroy(self, request, *args, **kwargs):
        """
        The leader of a team can not be removed from team members unless the team is deleted.
        """
        instance = self.get_object()
        if instance.team.leader == instance.employee and Team.objects.filter(id=instance.team.id).exists():
            return Response('A team leader can not be removed from the team.', status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().destroy(self, request, *args, **kwargs)
