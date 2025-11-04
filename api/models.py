from django.db import models

# Create your models here.
class Applicant(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    resume = models.FileField(upload_to='resumes',blank=True, null=True)
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Job(models.Model):
    id= models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()    
    posted_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    
class Application(models.Model):
    id= models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.applicant.name} applied for {self.job.title}"
  