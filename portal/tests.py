from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Student, Application, ReferralCode, Payment


class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.student = Student.objects.create(user=self.user, phone='08012345678')

    def test_student_creation(self):
        self.assertEqual(self.student.user.username, 'testuser')
        self.assertEqual(self.student.phone, '08012345678')
        self.assertFalse(self.student.has_paid)
        self.assertFalse(self.student.used_referral)


class ReferralCodeTest(TestCase):
    def setUp(self):
        self.code = ReferralCode.objects.create(code='CHSTH-TEST123')

    def test_referral_code_creation(self):
        self.assertEqual(self.code.code, 'CHSTH-TEST123')
        self.assertFalse(self.code.is_used)
        self.assertIsNone(self.code.used_by)


class ApplicationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.student = Student.objects.create(user=self.user, phone='08012345678')
        self.application = Application.objects.create(
            student=self.student,
            first_name='Test',
            surname='User'
        )

    def test_application_creation(self):
        self.assertIsNotNone(self.application.application_number)
        self.assertTrue(self.application.application_number.startswith('CHSTH/'))
        self.assertEqual(self.application.status, 'draft')


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CHSTH')

    def test_login_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_login_success(self):
        login = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login)
