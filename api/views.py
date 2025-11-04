from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from api.models import Applicant, Job, Application
from api.serializers import ApplicantSerializer, JobSerializer, ApplicationSerializer
from rest_framework.decorators import api_view


# Create your views here.
class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    
class ApplicationSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = [filters.SearchFilter]
    search_filds = ['name', 'email']
    
    
@api_view(['POST'])
def apply(request):
    applicant_id = request.data.get('applicant_id')
    job_id = request.data.get('job_id')

    if not applicant_id or not job_id:
        return Response(
            {"error": "applicant_id and job_id are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate applicant
    try:
        applicant = Applicant.objects.get(id=applicant_id)
    except Applicant.DoesNotExist:
        return Response(
            {"error": "Invalid applicant ID."}, status=status.HTTP_404_NOT_FOUND
        )

    # Validate job
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({"error": "Invalid job ID."}, status=status.HTTP_404_NOT_FOUND)

    # if already applied
    if Application.objects.filter(applicant_id=applicant_id, job_id=job_id).exists():
        return Response(
            {"message": "You have already applied for this job."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # create new application
    application = Application.objects.create(applicant=applicant, job=job)
    serializer = ApplicationSerializer(application)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
       
       
    