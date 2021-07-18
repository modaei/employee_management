from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from employment.api.serializers import WorkArrangementSerializer
from employment.models import Employee, WorkArrangement


class WorkArrangementCreateUpdateSetup(APITestCase):
    def setUp(self):
        super().setUp()
        self.employee_john = Employee.objects.create(name='John Doe', employee_id='123456', hourly_rate=17.3)
        self.employee_jane = Employee.objects.create(name='Jane Doe', employee_id='12345B', hourly_rate=11.3)

        # Valid payload. Should be able to create work arrangement successfully
        self.valid_payload_full_time = {
            'employee': self.employee_john.id,
            'type': 1
        }

        # Valid payload. Should be able to create work arrangement successfully
        self.valid_payload_part_time = {
            'employee': self.employee_john.id,
            'type': 2,
            'percentage': 40
        }

        # Invalid payload. Percentage less than 0
        self.invalid_payload_percentage_negative = {
            'employee': self.employee_john.id,
            'type': 2,
            'percentage': -40
        }

        # Invalid payload. Percentage bigger than 100
        self.invalid_payload_percentage_bigger_100 = {
            'employee': self.employee_john.id,
            'type': 2,
            'percentage': 140
        }

        # Invalid payload. Employee not defined
        self.invalid_payload_employee_not_present = {
            'type': 2,
            'percentage': 40
        }

        # Invalid payload. Part time assignment without percentage.
        self.invalid_payload_part_time_without_percentage = {
            'employee': self.employee_john.id,
            'type': 2
        }

        # Invalid payload. Employee not valid
        self.invalid_payload_employee_invalid = {
            'employee': 1000000,
            'type': 1
        }

        # Invalid payload. Employee is not a number
        self.invalid_payload_employee_not_number = {
            'employee': 'A1000000',
            'type': 1
        }


class WorkArrangementListGetDeleteSetup(APITestCase):
    def setUp(self):
        super().setUp()
        self.employee_john = Employee.objects.create(name='John Doe', employee_id='123456', hourly_rate=17.3)
        self.employee_jane = Employee.objects.create(name='Jane Doe', employee_id='12345B', hourly_rate=11.3)

        self.work_arrangement_john = WorkArrangement.objects.create(employee=self.employee_john,
                                                                    type=WorkArrangement.WorkTypes.FullTime)
        self.work_arrangement_jane = WorkArrangement.objects.create(employee=self.employee_jane,
                                                                    type=WorkArrangement.WorkTypes.PartTime,
                                                                    percentage=60)


class WorkArrangementCreateTests(WorkArrangementCreateUpdateSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:work_arrangement_list_create")

    def test_create_valid_work_arrangement_full_time(self):
        response = self.client.post(self.url, self.valid_payload_full_time, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkArrangement.objects.count(), 1)
        self.assertEqual(WorkArrangement.objects.first().type, self.valid_payload_full_time.get('type'))

    def test_create_valid_work_arrangement_part_time(self):
        response = self.client.post(self.url, self.valid_payload_part_time, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkArrangement.objects.count(), 1)
        self.assertEqual(WorkArrangement.objects.first().type, self.valid_payload_part_time.get('type'))

    def test_create_invalid_work_arrangement_new_arrangement_for_full_time_employee(self):
        self.client.post(self.url, self.valid_payload_full_time, format='json')
        response = self.client.post(self.url, self.valid_payload_part_time, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_work_arrangement_sum_percentages_bigger_100(self):
        self.client.post(self.url, self.valid_payload_part_time, format='json')
        self.client.post(self.url, self.valid_payload_part_time, format='json')
        response = self.client.post(self.url, self.valid_payload_part_time, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_work_arrangement_add_full_time_to_part_time(self):
        self.client.post(self.url, self.valid_payload_part_time, format='json')
        response = self.client.post(self.url, self.valid_payload_full_time, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_work_arrangement_percentage_negative(self):
        response = self.client.post(self.url, self.invalid_payload_percentage_negative, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_work_arrangement_percentage_bigger_100(self):
        response = self.client.post(self.url, self.invalid_payload_percentage_bigger_100, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_work_arrangement_employee_not_present(self):
        response = self.client.post(self.url, self.invalid_payload_employee_not_present, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_work_arrangement_part_time_without_percentage(self):
        response = self.client.post(self.url, self.invalid_payload_part_time_without_percentage, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_work_arrangement_employee_invalid(self):
        response = self.client.post(self.url, self.invalid_payload_employee_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_work_arrangement_employee_not_number(self):
        response = self.client.post(self.url, self.invalid_payload_employee_not_number, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WorkArrangementUpdateTests(WorkArrangementCreateUpdateSetup):
    def setUp(self):
        super().setUp()
        self.work_arrangement_full_time = WorkArrangement.objects.create(employee=self.employee_john,
                                                                         type=WorkArrangement.WorkTypes.FullTime)
        self.work_arrangement_part_time = WorkArrangement.objects.create(employee=self.employee_john,
                                                                         type=WorkArrangement.WorkTypes.FullTime,
                                                                         percentage=40)
        self.url_full_time = reverse("employment-api:work_arrangement_retrieve_update_destroy",
                                     kwargs={'pk': self.work_arrangement_full_time.pk})
        self.url_part_time = reverse("employment-api:work_arrangement_retrieve_update_destroy",
                                     kwargs={'pk': self.work_arrangement_part_time.pk})

    def test_update_valid_work_arrangement_full_time(self):
        response = self.client.put(self.url_full_time, self.valid_payload_part_time, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WorkArrangement.objects.count(), 2)
        self.assertEqual(WorkArrangement.objects.filter(id=self.work_arrangement_full_time.id).first().type,
                         self.valid_payload_part_time.get('type'))

    def test_update_valid_work_arrangement_part_time(self):
        response = self.client.put(self.url_part_time, self.valid_payload_full_time, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WorkArrangement.objects.count(), 2)
        self.assertEqual(
            WorkArrangement.objects.filter(id=self.work_arrangement_part_time.id).first().type,
            self.valid_payload_full_time.get('type'))

    def test_update_invalid_work_arrangement_percentage_negative(self):
        response = self.client.put(self.url_part_time, self.invalid_payload_percentage_negative, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_work_arrangement_percentage_bigger_100(self):
        response = self.client.put(self.url_part_time, self.invalid_payload_percentage_bigger_100, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_work_arrangement_employee_not_present(self):
        response = self.client.put(self.url_full_time, self.invalid_payload_employee_not_present, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_work_arrangement_part_time_without_percentage(self):
        response = self.client.put(self.url_part_time, self.invalid_payload_part_time_without_percentage, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_work_arrangement_employee_invalid(self):
        response = self.client.put(self.url_full_time, self.invalid_payload_employee_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_work_arrangement_employee_not_number(self):
        response = self.client.put(self.url_part_time, self.invalid_payload_employee_not_number, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WorkArrangementListTests(WorkArrangementListGetDeleteSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:work_arrangement_list_create")

    def test_get_all_work_arrangements(self):
        response = self.client.get(self.url)
        work_arrangements = WorkArrangement.objects.all().order_by('-create_date')
        serializer = WorkArrangementSerializer(work_arrangements, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class WorkArrangementGetTests(WorkArrangementListGetDeleteSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:work_arrangement_retrieve_update_destroy",
                           kwargs={'pk': self.work_arrangement_john.pk})

    def test_get_valid_single_employee(self):
        response = self.client.get(self.url)
        serializer = WorkArrangementSerializer(self.work_arrangement_john)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_employee(self):
        response = self.client.get(
            reverse("employment-api:work_arrangement_retrieve_update_destroy", kwargs={'pk': 1000000})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class WorkArrangementDeleteTests(WorkArrangementListGetDeleteSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:work_arrangement_retrieve_update_destroy",
                           kwargs={'pk': self.work_arrangement_john.id})

    def test_delete_valid_work_arrangement(self):
        response = self.client.delete(self.url)
        work_arrangement = WorkArrangement.objects.filter(id=self.work_arrangement_john.id).first()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(work_arrangement)

    def test_delete_invalid_work_arrangement(self):
        response = self.client.delete(
            reverse("employment-api:work_arrangement_retrieve_update_destroy", kwargs={'pk': 1000000})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
