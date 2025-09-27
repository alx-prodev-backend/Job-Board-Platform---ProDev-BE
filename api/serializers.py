from rest_framework import serializers
from .models import User, Company, Profile


###
# Serializers for displaying data
###

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'description', 'website', 'logo_url']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'headline', 'summary', 'resume_url', 'skills']
        depth = 1  # To show skill names instead of just IDs


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying a user's public information.
    It includes nested company or profile data based on the user's role.
    """
    # Using SerializerMethodField to dynamically choose which nested data to show
    details = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'details']

    def get_details(self, obj):
        if obj.role == User.Role.RECRUITTER:
            company = Company.objects.filter(user=obj).first()
            if company:
                return CompanySerializer(company).data
        elif obj.role == User.Role.JOB_SEEKER:
            profile = Profile.objects.filter(user=obj).first()
            if profile:
                return ProfileSerializer(profile).data
        return None


###
# Serializer for creating (registering) a new user
###

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. Handles creation of the user and
    their associated Company or Profile based on the role.
    """
    # We make the password write-only so it's not included in the response.
    password = serializers.CharField(write_only=True, required=True)
    company_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'company_name']

    def create(self, validated_data):
        # This create method is overridden to handle password hashing and
        # the creation of related Company/Profile objects.

        # Pop company_name as it's not a field on the User model
        company_name = validated_data.pop('company_name', None)
        role = validated_data.get('role')

        # Create the user instance
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],  # create_user handles hashing
            role=role
        )

        # Create Company or Profile based on the role
        if role == User.Role.RECRUITTER:
            if not company_name:
                raise serializers.ValidationError({"company_name": "Company name is required for recruiters."})
            Company.objects.create(user=user, name=company_name)

        elif role == User.Role.JOB_SEEKER:
            Profile.objects.create(user=user)

        return user