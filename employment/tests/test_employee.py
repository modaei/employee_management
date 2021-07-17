from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from employment.api.serializers import EmployeeSerializer
from employment.models import Employee


class EmployeeCreateUpdateSetup(APITestCase):
    def setUp(self):
        super().setUp()

        # Valid payload. Should be able to create employee successfully
        self.valid_payload = {
            'name': 'John Doe',
            'employee_id': 'a1234b',
            'hourly_rate': 12.25
        }

        # Invalid payload. Employee name is empty string
        self.invalid_payload_name_empty = {
            'name': '',
            'employee_id': 'a1234b',
            'hourly_rate': 12.25
        }

        # Invalid payload. Employee id is empty string
        self.invalid_payload_employee_id_empty = {
            'name': 'John Doe',
            'employee_id': '',
            'hourly_rate': 12.25
        }

        # Invalid payload. Employee hourly_rate is not specified
        self.invalid_payload_hourly_rate_not_present = {
            'name': 'John Doe',
            'employee_id': 'a1234b',
        }

        # Invalid payload. Employee name contains invalid character
        self.invalid_payload_name_invalid = {
            'name': 'John Doe!',
            'employee_id': 'a1234b',
            'hourly_rate': 12.25
        }

        # Invalid payload. employee_id contains invalid character
        self.invalid_payload_employee_id_invalid = {
            'name': 'John Doe',
            'employee_id': 'a1234b@',
            'hourly_rate': 12.25
        }

        # Invalid payload. hourly_rate is not a number
        self.invalid_payload_hourly_rate_not_number = {
            'name': 'John Doe',
            'employee_id': 'a1234b',
            'hourly_rate': '12.25b'
        }

        # Invalid payload. hourly_rate has too many digits
        self.invalid_payload_hourly_rate_too_many_digits = {
            'name': 'John Doe',
            'employee_id': 'a1234b',
            'hourly_rate': 12.255
        }


class EmployeeListGetDeleteSetup(APITestCase):
    def setUp(self):
        super().setUp()
        self.employee_john = Employee.objects.create(name='John Doe', employee_id='123456', hourly_rate=17.3)
        self.employee_jane = Employee.objects.create(name='Jane Doe', employee_id='12345B', hourly_rate=11.3)
        self.employee_jenny = Employee.objects.create(name='Jenny Doe', employee_id='A2345B', hourly_rate=18.6)

    def tearDown(self):
        Employee.objects.all().delete()
        super().tearDown()


class EmployeeCreateTests(EmployeeCreateUpdateSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:employee_list_create")

    def test_create_valid_employee(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get(employee_id='a1234b').name, 'John Doe')

    def test_create_invalid_employee_name_empty(self):
        response = self.client.post(self.url, self.invalid_payload_name_empty, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_employee_employee_id_empty(self):
        response = self.client.post(self.url, self.invalid_payload_employee_id_empty, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_employee_hourly_rate_not_present(self):
        response = self.client.post(self.url, self.invalid_payload_hourly_rate_not_present, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_employee_name_invalid(self):
        response = self.client.post(self.url, self.invalid_payload_name_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_employee_employee_id_invalid(self):
        response = self.client.post(self.url, self.invalid_payload_employee_id_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_employee_hourly_rate_not_number(self):
        response = self.client.post(self.url, self.invalid_payload_hourly_rate_not_number, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_employee_hourly_rate_too_many_digits(self):
        response = self.client.post(self.url, self.invalid_payload_hourly_rate_too_many_digits, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmployeeUpdateTests(EmployeeCreateUpdateSetup):
    def setUp(self):
        super().setUp()
        self.employee = Employee.objects.create(name='Jane Doe', employee_id='123456', hourly_rate=17.3)
        self.url = reverse("employment-api:employee_retrieve_update_destroy", kwargs={'pk': self.employee.pk})

    def test_update_valid_employee(self):
        response = self.client.put(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get(employee_id='a1234b').name, 'John Doe')

    def test_update_invalid_employee_name_empty(self):
        response = self.client.put(self.url, self.invalid_payload_name_empty, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_employee_employee_id_empty(self):
        response = self.client.put(self.url, self.invalid_payload_employee_id_empty, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_employee_hourly_rate_not_present(self):
        response = self.client.put(self.url, self.invalid_payload_hourly_rate_not_present, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_employee_name_invalid(self):
        response = self.client.put(self.url, self.invalid_payload_name_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_employee_employee_id_invalid(self):
        response = self.client.put(self.url, self.invalid_payload_employee_id_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_employee_hourly_rate_not_number(self):
        response = self.client.put(self.url, self.invalid_payload_hourly_rate_not_number, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_employee_hourly_rate_too_many_digits(self):
        response = self.client.put(self.url, self.invalid_payload_hourly_rate_too_many_digits, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmployeeListTests(EmployeeListGetDeleteSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:employee_list_create")

    def test_get_all_employees(self):
        response = self.client.get(self.url)
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class EmployeeGetTests(EmployeeListGetDeleteSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:employee_retrieve_update_destroy", kwargs={'pk': self.employee_jane.pk})

    def test_get_valid_single_employee(self):
        response = self.client.get(self.url)
        serializer = EmployeeSerializer(self.employee_jane)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_employee(self):
        response = self.client.get(
            reverse("employment-api:employee_retrieve_update_destroy", kwargs={'pk': 1000000})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EmployeeDeleteTests(EmployeeListGetDeleteSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:employee_retrieve_update_destroy", kwargs={'pk': self.employee_jane.pk})

    def test_delete_valid_employee(self):
        response = self.client.delete(self.url)
        employee = Employee.objects.filter(id=self.employee_jane.pk).first()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(employee)

    def test_delete_invalid_employee(self):
        response = self.client.delete(
            reverse("employment-api:employee_retrieve_update_destroy", kwargs={'pk': 1000000})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
