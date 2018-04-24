from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email as valid_email
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from .models import OfpptID, User

class OfpptSerializer(serializers.Serializer):
    mat = serializers.CharField()

    def validate_mat(self, mat):
        try:
            ofp = OfpptID.objects.get(mat=mat)
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError('Invalid ofppt ID')
        return mat

class RegisterSerializer(serializers.Serializer):
    ofppt = OfpptSerializer()
    email = serializers.EmailField()
    first_name = serializers.CharField(min_length=3, max_length=20)
    last_name = serializers.CharField(min_length=3, max_length=20)
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate_password1(self, password1):
        print('validat password called')
        validate_password(password1)
        return password1

    def validate(self, data):
        print('validate called')
        
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def create(self, validated_data):
        print('create called')
        ofppt = validated_data.get('ofppt')
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        password = validated_data.get('password1')
        ofp = OfpptID.objects.get(mat=ofppt.get('mat'))
        ofp.verified = True
        ofp.save()
        u = User(ofppt=ofp, email=email, first_name=first_name, last_name=last_name)
        u.set_password(password)
        u.save()
        return u