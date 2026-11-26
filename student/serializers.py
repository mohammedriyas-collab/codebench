from rest_framework import serializers
from api.models import User
from student.models import StudentProfile,Submission

class SignUpSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields=["id","username","email","password","phone"]


    def create(self, validated_data):    # to encrypt password
        return User.objects.create_user(**validated_data)

class StudentprofileSerializer(serializers.ModelSerializer):

    class Meta:

        model = StudentProfile

        fields = "__all__"

        read_only_fields=["id","user","created_at","updated_at"]

class SubmissionSerializer(serializers.ModelSerializer):

    class Meta:

        model = Submission
        
        fields = "__all__"

        read_only_fields =["id","submitted_by","problem","status","created_at","updated_at","remarks","score"]