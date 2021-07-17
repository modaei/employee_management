from rest_framework.serializers import (ModelSerializer, SerializerMethodField, ValidationError)
from ..models import Team, Employee, TeamEmployee
import re
from rest_framework.validators import UniqueTogetherValidator


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
                message='This employee is already added to this group.'
            )
        ]

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())

    def to_representation(self, instance):
        """
        Allows to send the team and employee's id as 'team' and 'employee' in PUT and POST
        (Instead of 'team_id' and 'employee_id').
        """
        self.fields['employee'] = EmployeeSerializer()
        self.fields['team'] = TeamSerializer()
        return super(TeamEmployeeSerializer, self).to_representation(instance)
