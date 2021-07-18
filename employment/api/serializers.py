from rest_framework.serializers import (ModelSerializer, SerializerMethodField, ValidationError, Serializer,
                                        DecimalField)
from ..models import Team, Employee, TeamEmployee, WorkArrangement
import re
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Sum


class EmployeeBriefSerializer(ModelSerializer):
    """
    Serializes employee objects with minimal info to include in team members info.
    """
    create_date = SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'create_date', 'name', 'employee_id']
        read_only_fields = ['id', 'name', 'create_date', 'employee_id']

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())


class TeamBriefSerializer(ModelSerializer):
    """
    Serializes team objects with minimal info to include in employees team info.
    """
    create_date = SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'create_date']
        read_only_fields = ['id', 'name', 'create_date']

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())

    def get_update_date(self, obj):
        return int(obj.update_date.timestamp())


class EmployeeSerializer(ModelSerializer):
    """
    Serializes employee objects
    """
    create_date = SerializerMethodField()
    update_date = SerializerMethodField()
    teams = TeamBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['id', 'teams', 'create_date', 'update_date']

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())

    def get_update_date(self, obj):
        return int(obj.update_date.timestamp())

    def validate_name(self, value):
        if re.match("^[a-zA-Z0-9_ ]*$", value):
            return value
        else:
            raise ValidationError("Employee name can only contain alphabetic characters, numbers, spaces and _.")

    def validate_employee_id(self, value):
        if re.match("^[a-zA-Z0-9_]*$", value):
            return value
        else:
            raise ValidationError("Employee_ID can only contain alphabetic characters, numbers and _.")


class TeamSerializer(ModelSerializer):
    """
    Serializes team objects.
    """
    create_date = SerializerMethodField()
    update_date = SerializerMethodField()
    members = EmployeeBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['id', 'members', 'create_date', 'update_date']

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())

    def get_update_date(self, obj):
        return int(obj.update_date.timestamp())

    def to_representation(self, instance):
        """
        Allows to send the leader's id as 'leader' in PUT and POST (Instead of 'leader_id').
        """
        self.fields['leader'] = EmployeeBriefSerializer()
        return super(TeamSerializer, self).to_representation(instance)

    def validate_name(self, value):
        if re.match("^[a-zA-Z0-9_ ]*$", value):
            return value
        else:
            raise ValidationError("Team name can only contain alphabetic characters, numbers, spaces and _.")


class TeamEmployeeSerializer(ModelSerializer):
    """
    Serializes team objects.
    """
    create_date = SerializerMethodField()

    class Meta:
        model = TeamEmployee
        fields = '__all__'
        read_only_fields = ['id', 'create_date']
        validators = [
            UniqueTogetherValidator(
                queryset=TeamEmployee.objects.all(),
                fields=('employee', 'team'),
                message='This employee is already added to this team.'
            )
        ]

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())

    def to_representation(self, instance):
        """
        Allows to send the team and employee's id as 'team' and 'employee' in PUT and POST
        (Instead of 'team_id' and 'employee_id').
        """
        self.fields['employee'] = EmployeeBriefSerializer()
        self.fields['team'] = TeamBriefSerializer()
        return super(TeamEmployeeSerializer, self).to_representation(instance)


class WorkArrangementSerializer(ModelSerializer):
    """
    Serializes WorkArrangement objects.
    """
    create_date = SerializerMethodField()
    update_date = SerializerMethodField()

    class Meta:
        model = WorkArrangement
        fields = '__all__'
        read_only_fields = ['id', 'create_date', 'update_date']

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())

    def get_update_date(self, obj):
        return int(obj.update_date.timestamp())

    def validate(self, attrs):
        """
        If WorkArrangement is full time, user must have no other work arrangements. (On create only)
        If WorkArrangement is part time, percentage is mandatory. (On create and update)
        If WorkArrangement is part time, user must not have a full time job. (On create only)
        If WorkArrangement is part time, sum of all user work arrangement percentages must be less than or equal 100.
        (On create and update)
        """
        if attrs['type'] == WorkArrangement.WorkTypes.FullTime:
            if WorkArrangement.objects.filter(employee_id=attrs['employee']).exists() and not self.instance:
                raise ValidationError("Employee already has another work assignment.")
        elif attrs['type'] == WorkArrangement.WorkTypes.PartTime:
            if 'percentage' not in attrs or attrs['percentage'] is None:
                raise ValidationError("Percentage should be specified for work assignments.")
            work_arrangements = WorkArrangement.objects.filter(employee_id=attrs['employee']).all()
            if any(work_arrangement.type == WorkArrangement.WorkTypes.FullTime for work_arrangement in
                   work_arrangements) and not self.instance:
                raise ValidationError("User already has a full time work assignment.")
            sum_percentage = WorkArrangement.objects.filter(employee_id=attrs['employee']).aggregate(Sum('percentage'))[
                'percentage__sum']
            if sum_percentage is not None and sum_percentage + int(attrs['percentage']) > 100:
                raise ValidationError("Sum of user work assignment percentages can not exceed 100.")
        return attrs

    def to_representation(self, instance):
        """
        Allows to send the employee's id as 'employee' in PUT and POST (Instead of 'employee_id').
        """
        self.fields['employee'] = EmployeeBriefSerializer()
        return super(WorkArrangementSerializer, self).to_representation(instance)


class SalarySerializer(Serializer):
    employee = EmployeeBriefSerializer()
    payable = DecimalField(max_digits=5, decimal_places=2)
