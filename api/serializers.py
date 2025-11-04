from rest_framework import serializers
from api.models import Applicant, Job, Application


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'
        
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application 
        fields = '__all__'