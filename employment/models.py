from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Employee(models.Model):
    name = models.CharField(blank=False, null=False, max_length=settings.NAME_MAX_LEN, db_index=True)
    # The company identification number of the employee(personal number). Not to be mixed with the model's primary key.
    employee_id = models.CharField(blank=False, null=False, max_length=settings.EMPLOYEE_ID_MAX_LEN, db_index=True)
    # Employee's hourly wage
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created")
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="Last updated")
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
    members = models.ManyToManyField(Employee, through='TeamEmployee')


class TeamEmployee(models.Model):
    """
    Represents membership of an employee in a team.
    """
    employee = models.ForeignKey(Employee, blank=False, null=False, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, blank=False, null=False, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created")


@receiver(post_save, sender=Team)
def add_leader_to_team(sender, instance, **kwargs):
    """
    The team leader should always be a member of the team.
    So if he is not he will be automatically be added to the team.
    """
    team_employee = TeamEmployee.objects.filter(team=instance).filter(employee=instance.leader).first()
    if team_employee is None:
        TeamEmployee.objects.create(team=instance, employee=instance.leader)
