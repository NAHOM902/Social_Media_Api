from rest_framework import serializers
from .models import User
from phonenumber_field.serializerfields import PhoneNumberField




class RegistrationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=25)
    email = serializers.CharField(max_length=80)
    password = serializers.CharField(min_length=5)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']


    def validate(self, attrs):
        
        username_exists = User.objects.filter(username=attrs['username']).exists()
        if username_exists:
            raise serializers.ValidationError("user with this name already exists")
        
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise serializers.ValidationError("user with such eamil already exists")

        phone_number_exists = User.objects.filter(phone_number=attrs['phone_number']).exists()
        if phone_number_exists:
            raise serializers.ValidationError("user with such phone_number already exists")


        return super().validate(attrs)