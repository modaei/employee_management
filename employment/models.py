from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator
from decimal import Decimal
from django.db.models import Sum


class Employee(models.Model):
    """
    Represents an employee.
    """
    name = models.CharField(blank=False, null=False, max_length=settings.NAME_MAX_LEN, db_index=True)
    # The company identification number of the employee(personal number). Not to be mixed with the model's primary key.
    employee_id = models.CharField(blank=False, null=False, max_length=settings.EMPLOYEE_ID_MAX_LEN, db_index=True)
    # Employee's hourly wage
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created")
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="Last updated")
    # The teams that the employee is a member of.
    teams = models.ManyToManyField('Team', through='TeamEmployee')


class Team(models.Model):
    """
    Represents a team of employees
    """
    name = models.CharField(blank=False, null=False, max_length=settings.NAME_MAX_LEN, db_index=True)
    leader = models.ForeignKey(Employee, blank=False, null=False, on_delete=models.PROTECT,
                               related_name="team_leader_employee")
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created")
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="Last updated")
    # Employees who are a member of this team.
    members = models.ManyToManyField(Employee, through='TeamEmployee')


class TeamEmployee(models.Model):
    """
    Represents membership of an employee in a team.
    """
    employee = models.ForeignKey(Employee, blank=False, null=False, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, blank=False, null=False, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created")


class WorkArrangement(models.Model):
    """
    Represents a work arrangement for an employee
    """

    class WorkTypes(models.IntegerChoices):
        FullTime = 1
        PartTime = 2

    employee = models.ForeignKey(Employee, blank=False, null=False, on_delete=models.CASCADE)
    type = models.IntegerField(choices=WorkTypes.choices, null=False, blank=False)
    percentage = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(100), ])
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created")
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="Last updated")


class Salary(object):
    """
    Takes an employee as a parameter in the constructor and then calculates the salary of
    the employee and stores it in self.payable variable automatically.
    """
    employee = models.ForeignKey(Employee, blank=False, null=False, on_delete=models.CASCADE)
    payable = 0

    def calculate_payable(self):
        """
        calculates the salary of the employee based on his work arrangements.
        """
        full_time_hours = Decimal(settings.FULL_TIME_HOURS)
        leader_coefficient = Decimal(settings.LEADER_COEFFICIENT)

        is_leader = any(team.leader == self.employee for team in self.employee.teams.all())
        hourly_rate = Decimal(self.employee.hourly_rate)
        # If an employee is a leader in any group, his hourly wage should be multiplied to a coefficient.
        if is_leader:
            hourly_rate = leader_coefficient * hourly_rate

        work_arrangements = WorkArrangement.objects.filter(employee=self.employee).all()
        if work_arrangements.count() > 0:
            # If the employee has a full time work arrangement, he has no other work arrangements.
            if work_arrangements.first().type == WorkArrangement.WorkTypes.FullTime:
                self.payable = full_time_hours * hourly_rate
            else:
                # If the employee has a part time work arrangement, he may have other work arrangements too.
                sum_percentage = work_arrangements.aggregate(Sum('percentage'))['percentage__sum']
                self.payable = Decimal(sum_percentage / 100) * full_time_hours * hourly_rate

    def __init__(self, employee, *args, **kwargs):
        self.employee = employee
        self.calculate_payable()


@receiver(post_save, sender=Team)
def add_leader_to_team(sender, instance, **kwargs):
    """
    The team leader should always be a member of the team.
    So if he is not he will be automatically be added to the team.
    """
    team_employee = TeamEmployee.objects.filter(team=instance).filter(employee=instance.leader).first()
    if team_employee is None:
        TeamEmployee.objects.create(team=instance, employee=instance.leader)


@receiver(pre_save, sender=WorkArrangement)
def set_percentage_none_for_full_time_arrangements(sender, instance, **kwargs):
    """
    If a job is full time the value for percentage will be ignored and always be set to None
    """
    if instance.type == WorkArrangement.WorkTypes.FullTime:
        instance.percentage = None
