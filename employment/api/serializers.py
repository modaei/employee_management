from rest_framework.serializers import (ModelSerializer, SerializerMethodField, )
from ..models import Employee


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