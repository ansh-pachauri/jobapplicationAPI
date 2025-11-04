from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Applicant, Job, Application


class ApplyToJobTests(APITestCase):
    def setUp(self):
        """Setup test data for apply endpoint tests."""
        # Create a test user
        self.user = User.objects.create_user(
            username="ansh", email="ansh@example.com", password="password123"
        )

        # Create an Applicant explicitly 
        self.applicant = Applicant.objects.create(
            name=self.user.username, email=self.user.email
        )

        # Create a test job
        self.job = Job.objects.create(title="Backend Developer", description="Build Django APIs")

        # Prepare auth token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Authenticated client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Endpoint URL
        self.url = reverse("apply")

    def test_apply_successfully(self):
        """User can apply to a job successfully when authenticated and payload is valid."""
        payload = {"applicant_id": self.applicant.id, "job_id": self.job.id}
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "applied")
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.first().applicant, self.applicant)

    def test_apply_without_authentication(self):
        """Unauthenticated users cannot apply (default permission requires auth)."""
        self.client.credentials()  # remove token
        payload = {"applicant_id": self.applicant.id, "job_id": self.job.id}
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_apply_without_job_id(self):
        """Applying without job_id or applicant_id should return 400."""
        payload = {"applicant_id": self.applicant.id}
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "applicant_id and job_id are required.")

    def test_apply_with_invalid_job(self):
        """Applying to a non-existent job should return 404."""
        payload = {"applicant_id": self.applicant.id, "job_id": 9999}
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Invalid job ID.")

    def test_apply_twice_to_same_job(self):
        """Applying twice to the same job should fail on the second attempt."""
        payload = {"applicant_id": self.applicant.id, "job_id": self.job.id}

        # First application
        resp1 = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp1.status_code, status.HTTP_201_CREATED)

        # Second attempt
        resp2 = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp2.data["message"], "You have already applied for this job.")
        self.assertEqual(Application.objects.count(), 1)
