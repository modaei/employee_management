from rest_framework.serializers import (ModelSerializer, SerializerMethodField, ValidationError)
from ..models import Employee
import re


class EmployeeSerializer(ModelSerializer):
    """
    Serializes employee objects
    """
    create_date = SerializerMethodField()
    update_date = SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['id', 'create_date', 'update_date']

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
