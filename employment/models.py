from django.db import models
from django.conf import settings


class Employee(models.Model):
    name = models.CharField(blank=False, null=False, max_length=settings.NAME_MAX_LEN, db_index=True)
    # The company identification number of the employee(personal number). Not to be mixed with the model's primary key.
    employee_id = models.CharField(blank=False, null=False, max_length=settings.EMPLOYEE_ID_MAX_LEN, db_index=True)
    # Employee's hourly wage
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created")
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="Last updated")