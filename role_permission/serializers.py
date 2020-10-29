from rest_framework import serializers
from .models import *
from blueapps.account.models import User

class MenuSerializers(serializers.ModelSerializer):
    # role = serializers.CharField(source='role.name')

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name",instance.name)
        instance.menu_parameter = validated_data.get("menu_parameter",instance.menu_parameter)
        instance.level = validated_data.get("level",instance.level)
        instance.father_menu = validated_data.get("father_menu",instance.father_menu)
        instance.save()
        return instance

    class Meta:
        model = Menu
        fields = "__all__"

class MenuSecondSerializers(serializers.ModelSerializer):
    # role = serializers.CharField(source='role.name')

    class Meta:
        model = Menu
        fields = ["name"]

class PermissionSerializers(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['title']

class RoleSerializers(serializers.ModelSerializer):

    permission = PermissionSerializers(many=True)
    menu= MenuSecondSerializers(many=True)
    class Meta:
        model = Role
        fields = "__all__"


class UserRoleSerializers(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    role = serializers.CharField(source='role.name')

    class Meta:
        model = UserRole
        fields = "__all__"
        # depth = 1