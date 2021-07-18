from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from employment.api.serializers import SalarySerializer
from employment.models import Employee, WorkArrangement, Salary


class SalaryListGetSetup(APITestCase):
    def setUp(self):
        """
        Create two employees and one work arrangement for each to use in list all salaries and get a single salary test.
        """
        super().setUp()
        self.employee_john = Employee.objects.create(name='John Doe', employee_id='123456', hourly_rate=17.3)
        self.employee_jane = Employee.objects.create(name='Jane Doe', employee_id='12345B', hourly_rate=11.3)

        self.work_arrangement_john = WorkArrangement.objects.create(employee=self.employee_john,
                                                                    type=WorkArrangement.WorkTypes.FullTime)
        self.work_arrangement_jane = WorkArrangement.objects.create(employee=self.employee_jane,
                                                                    type=WorkArrangement.WorkTypes.PartTime,
                                                                    percentage=60)


class SalaryListTests(SalaryListGetSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse("employment-api:salary_list")

    def test_get_all_salaries(self):
        """
        Get the list of all employees with their salaries.
        """
        response = self.client.get(self.url)
        employees = Employee.objects.all()
        salaries = [Salary(employee=employee) for employee in employees]
        serializer = SalarySerializer(salaries, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class SalaryGetTests(SalaryListGetSetup):
    def setUp(self):
        super().setUp()
        base_url = reverse("employment-api:salary_list")
        self.url = f'{base_url}?employee={self.employee_john.pk}'

    def test_get_valid_single_employee_salary(self):
        """
        Get salary of a single employee
        """
        response = self.client.get(self.url)
        serializer = SalarySerializer(Salary(employee=self.employee_john))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_employee_salary(self):
        """
        Get salary for an ID which does not exist.
        """
        response = self.client.get(f'{reverse("employment-api:salary_list")}?employee=1000000')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
