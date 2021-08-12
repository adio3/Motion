from rest_framework import serializers

from .models import Reg_profile


class Reg_profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reg_profile
        fields = ['email', 'code']
        # read_only_fields = ['user']

# class Reg_profileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reg_profile
#         fields = ['code']
#         # read_only_fields = ['email']
