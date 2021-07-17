from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from employment.api.serializers import TeamSerializer
from employment.models import Employee, Team


class TeamCreateUpdateSetup(APITestCase):
    def setUp(self):
        super().setUp()
        self.employee_john = Employee.objects.create(name='John Doe', employee_id='123456', hourly_rate=17.3)
        self.employee_jane = Employee.objects.create(name='Jane Doe', employee_id='12345B', hourly_rate=11.3)

        # Valid payload. Should be able to create team successfully
        self.valid_payload = {
            'name': 'Back end',
            'leader': self.employee_john.id
        }

        # Invalid payload. Team name is empty string
        self.invalid_payload_name_empty = {
            'name': '',
            'leader': self.employee_john.id
        }

        # Invalid payload. Leader not defined
        self.invalid_payload_leader_not_present = {
            'name': 'Back end',
        }

        # Invalid payload. Team name contains invalid character
        self.invalid_payload_name_invalid = {
            'name': 'Back end!',
            'leader': self.employee_john.id
        }

        # Invalid payload. Leader not valid
        self.invalid_payload_leader_invalid = {
            'name': 'Back end',
            'leader': 1000000
        }

        # Invalid payload. Leader is not a number
        self.invalid_payload_leader_not_number = {
            'name': 'Back end',
            'leader': 'leader'

        }

    def tearDown(self):
        Team.objects.all().delete()
        Employee.objects.all().delete()
        super().tearDown()


class TeamListGetDeleteSetup(APITestCase):
    def setUp(self):
        super().setUp()
        self.employee_john = Employee.objects.create(name='John Doe', employee_id='123456', hourly_rate=17.3)
        self.employee_jane = Employee.objects.create(name='Jane Doe', employee_id='12345B', hourly_rate=11.3)

        self.team_backend = Team.objects.create(name='Back end', leader=self.employee_john)
        self.team_frontend = Team.objects.create(name='Front end', leader=self.employee_jane)

    def tearDown(self):
        Team.objects.all().delete()
        Employee.objects.all().delete()
        super().tearDown()


class TeamCreateTests(TeamCreateUpdateSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:team_list_create")

    def test_create_valid_team(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get(name='Back end').leader, self.employee_john)

    def test_create_invalid_team_name_empty(self):
        response = self.client.post(self.url, self.invalid_payload_name_empty, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_team_leader_not_present(self):
        response = self.client.post(self.url, self.invalid_payload_leader_not_present, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_team_name_invalid(self):
        response = self.client.post(self.url, self.invalid_payload_name_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_team_leader_invalid(self):
        response = self.client.post(self.url, self.invalid_payload_leader_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_team_leader_not_number(self):
        response = self.client.post(self.url, self.invalid_payload_leader_not_number, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TeamUpdateTests(TeamCreateUpdateSetup):
    def setUp(self):
        super().setUp()
        self.team = Team.objects.create(name='Front end', leader=self.employee_jane)
        self.url = reverse("employment-api:team_retrieve_update_destroy", kwargs={'pk': self.team.pk})

    def test_update_valid_team(self):
        response = self.client.put(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get(name='Back end').leader, self.employee_john)

    def test_update_invalid_team_name_empty(self):
        response = self.client.put(self.url, self.invalid_payload_name_empty, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_team_leader_not_present(self):
        response = self.client.put(self.url, self.invalid_payload_leader_not_present, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_team_name_invalid(self):
        response = self.client.put(self.url, self.invalid_payload_name_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_team_leader_invalid(self):
        response = self.client.put(self.url, self.invalid_payload_leader_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_team_leader_not_number(self):
        response = self.client.put(self.url, self.invalid_payload_leader_not_number, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TeamListTests(TeamListGetDeleteSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:team_list_create")

    def test_get_all_teams(self):
        response = self.client.get(self.url)
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class TeamGetTests(TeamListGetDeleteSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:team_retrieve_update_destroy", kwargs={'pk': self.team_backend.pk})

    def test_get_valid_single_employee(self):
        response = self.client.get(self.url)
        serializer = TeamSerializer(self.team_backend)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_employee(self):
        response = self.client.get(
            reverse("employment-api:team_retrieve_update_destroy", kwargs={'pk': 1000000})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TeamDeleteTests(TeamListGetDeleteSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:team_retrieve_update_destroy", kwargs={'pk': self.team_backend.pk})

    def test_delete_valid_team(self):
        response = self.client.delete(self.url)
        team = Team.objects.filter(id=self.employee_jane.pk).first()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(team)

    def test_delete_invalid_team(self):
        response = self.client.delete(
            reverse("employment-api:team_retrieve_update_destroy", kwargs={'pk': 1000000})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
