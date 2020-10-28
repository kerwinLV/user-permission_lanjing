from rest_framework import serializers
from .models import *


class MenuSerializers(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name')

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name",instance.name)
        instance.menu_parameter = validated_data.get("menu_parameter",instance.menu_parameter)
        instance.level = validated_data.get("level",instance.level)
        instance.father_menu = validated_data.get("father_menu",instance.father_menu)
        instance.role = validated_data.get(self.context["role"],instance.role)
        instance.save()
        return instance

    class Meta:
        model = Menu
        fields = "__all__"

class PermissionSerializers(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['title']

class RoleSerializers(serializers.ModelSerializer):

    permission = PermissionSerializers(many=True)
    class Meta:
        model = Role
        fields = "__all__"

