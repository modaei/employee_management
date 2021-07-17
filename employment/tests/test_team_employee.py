from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from employment.api.serializers import TeamEmployeeSerializer
from employment.models import Employee, Team, TeamEmployee


class TeamEmployeeCreateUpdateSetup(APITestCase):
    def setUp(self):
        super().setUp()
        self.employee_john = Employee.objects.create(name='John Doe', employee_id='123456', hourly_rate=17.3)
        self.employee_jane = Employee.objects.create(name='Jane Doe', employee_id='12345B', hourly_rate=11.3)
        self.employee_david = Employee.objects.create(name='David Doe', employee_id='12345C', hourly_rate=14.8)

        self.team_back_end = Team.objects.create(name='Back end', leader=self.employee_john)

        # Valid payload. Should be able to create TeamEmployee successfully
        self.valid_payload = {
            'team': self.team_back_end.id,
            'employee': self.employee_jane.id,
        }

        # Invalid payload. Team not defined
        self.invalid_payload_team_not_defined = {
            'employee': self.employee_jane.id,
        }

        # Invalid payload. Employee not defined
        self.invalid_payload_employee_not_defined = {
            'team': self.team_back_end.id,
        }

        # Invalid payload. Team is not a number
        self.invalid_payload_team_not_number = {
            'team': 'Back end!',
            'employee': self.employee_jane.id,
        }

        # Invalid payload. Team not valid
        self.invalid_payload_team_invalid = {
            'team': 1000000,
            'employee': self.employee_jane.id,
        }

        # Invalid payload. Adding team leader as a member.
        self.invalid_payload_add_leader_as_member = {
            'team': self.team_back_end.id,
            'employee': self.employee_john.id,

        }


class TeamEmployeeListGetDeleteSetup(APITestCase):
    def setUp(self):
        super().setUp()
        self.employee_john = Employee.objects.create(name='John Doe', employee_id='123456', hourly_rate=17.3)
        self.employee_jane = Employee.objects.create(name='Jane Doe', employee_id='12345B', hourly_rate=11.3)

        self.team_backend = Team.objects.create(name='Back end', leader=self.employee_john)
        self.team_employee = TeamEmployee.objects.create(team=self.team_backend, employee=self.employee_jane)


class TeamEmployeeCreateTests(TeamEmployeeCreateUpdateSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:team_employee_list_create")

    def test_create_valid_team_employee(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TeamEmployee.objects.count(), 2)
        self.assertEqual(TeamEmployee.objects.get(employee__name=self.employee_jane.name).team, self.team_back_end)

    def test_create_invalid_team_employee_team_not_defined(self):
        response = self.client.post(self.url, self.invalid_payload_team_not_defined, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_team_employee_employee_not_defined(self):
        response = self.client.post(self.url, self.invalid_payload_employee_not_defined, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_team_employee_team_not_number(self):
        response = self.client.post(self.url, self.invalid_payload_team_not_number, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_team_employee_team_invalid(self):
        response = self.client.post(self.url, self.invalid_payload_team_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_team_employee_add_leader_as_member(self):
        response = self.client.post(self.url, self.invalid_payload_add_leader_as_member, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TeamEmployeeUpdateTests(TeamEmployeeCreateUpdateSetup):
    def setUp(self):
        super().setUp()
        self.team_employee = TeamEmployee.objects.create(team=self.team_back_end, employee=self.employee_david)
        self.url = reverse("employment-api:team_employee_retrieve_update_destroy", kwargs={'pk': self.team_employee.pk})

    def test_update_valid_team_employee(self):
        response = self.client.put(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TeamEmployee.objects.count(), 2)
        self.assertEqual(TeamEmployee.objects.get(id=self.team_employee.id).employee, self.employee_jane)

    def test_update_invalid_team_employee_team_not_defined(self):
        response = self.client.put(self.url, self.invalid_payload_team_not_defined, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_team_employee_employee_not_defined(self):
        response = self.client.put(self.url, self.invalid_payload_employee_not_defined, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_team_employee_team_not_number(self):
        response = self.client.put(self.url, self.invalid_payload_team_not_number, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_team_employee_team_invalid(self):
        response = self.client.put(self.url, self.invalid_payload_team_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_team_employee_add_leader_as_member(self):
        response = self.client.put(self.url, self.invalid_payload_add_leader_as_member, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TeamEmployeeListTests(TeamEmployeeListGetDeleteSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:team_employee_list_create")

    def test_get_all_teams(self):
        response = self.client.get(self.url)
        team_employees = TeamEmployee.objects.all().order_by('-create_date')
        serializer = TeamEmployeeSerializer(team_employees, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class TeamEmployeeGetTests(TeamEmployeeListGetDeleteSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:team_employee_retrieve_update_destroy", kwargs={'pk': self.team_employee.id})

    def test_get_valid_single_employee(self):
        response = self.client.get(self.url)
        serializer = TeamEmployeeSerializer(self.team_employee)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_employee(self):
        response = self.client.get(
            reverse("employment-api:team_employee_retrieve_update_destroy", kwargs={'pk': 1000000})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TeamEmployeeDeleteTests(TeamEmployeeListGetDeleteSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:team_employee_retrieve_update_destroy", kwargs={'pk': self.team_employee.pk})

    def test_delete_valid_team_employee(self):
        response = self.client.delete(self.url)
        team_employee = TeamEmployee.objects.filter(id=self.employee_jane.pk).first()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(team_employee)

    def test_delete_invalid_team_employee(self):
        response = self.client.delete(
            reverse("employment-api:team_employee_retrieve_update_destroy", kwargs={'pk': 1000000})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_invalid_remove_leader_from_team(self):
        team_employee = TeamEmployee.objects.get(employee__employee_id=self.employee_john.employee_id)
        response = self.client.delete(
            reverse("employment-api:team_employee_retrieve_update_destroy", kwargs={'pk': team_employee.id})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
