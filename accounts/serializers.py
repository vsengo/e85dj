from .models import Member
from django.contrib.auth.models import User

from rest_framework import serializers

class MemberPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Member
        fields = ['mobile']

class MemberSerializer(serializers.ModelSerializer):
    # mobile = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='mobile'
    #  )
    #profile = serializers.StringRelatedField(many=True)
    class Meta:
        model  = User
        fields = ['first_name','last_name','email']