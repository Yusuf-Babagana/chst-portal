from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string


class ReferralCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {'Used' if self.is_used else 'Available'}"

    class Meta:
        verbose_name = "Referral Code"
        verbose_name_plural = "Referral Codes"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    has_paid = models.BooleanField(default=False)
    used_referral = models.BooleanField(default=False)
    referral_code = models.ForeignKey(ReferralCode, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    paystack_reference = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.email} - {self.amount} - {self.status}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-created_at']


class Application(models.Model):
    APPLICATION_STATUS = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    COURSES = (
        ('diploma_schew', 'Diploma in Community Health (SCHEW)'),
        ('certificate_jchew', 'Certificate in Community Health (JCHEW)'),
        ('diploma_him', 'Diploma in Health Information Management'),
        ('diploma_env_health', 'Diploma in Environmental Health'),
        ('diploma_xray', 'Diploma in X-Ray and Imaging'),
        ('diploma_nutrition', 'Diploma in Nutrition and Dietetics'),
        ('retraining_jchew', 'Retraining in Community Health (JCHEW holders)'),
    )

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='application')
    application_number = models.CharField(max_length=20, unique=True, blank=True)

    passport_photo = models.ImageField(upload_to='passports/', blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    other_names = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    lga = models.CharField(max_length=100, blank=True)
    state_of_origin = models.CharField(max_length=100, blank=True)

    guardian_name = models.CharField(max_length=200, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    guardian_address = models.TextField(blank=True)
    guardian_relationship = models.CharField(max_length=100, blank=True)

    section_a_completed = models.BooleanField(default=False)
    section_b_completed = models.BooleanField(default=False)
    section_c_completed = models.BooleanField(default=False)
    section_d_completed = models.BooleanField(default=False)
    section_e_completed = models.BooleanField(default=False)

    first_choice = models.CharField(max_length=50, choices=COURSES, blank=True)
    second_choice = models.CharField(max_length=50, choices=COURSES, blank=True)

    declaration_text = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.application_number:
            year = timezone.now().year
            random_num = ''.join(random.choices(string.digits, k=6))
            self.application_number = f"CHSTH/{year}/{random_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.application_number} - {self.student.user.get_full_name()}"

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        ordering = ['-created_at']


class SchoolAttended(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='schools_attended')
    school_name = models.CharField(max_length=200, blank=True)
    from_year = models.CharField(max_length=4, blank=True)
    to_year = models.CharField(max_length=4, blank=True)

    def __str__(self):
        return f"{self.school_name} ({self.from_year} - {self.to_year})"

    class Meta:
        verbose_name = "School Attended"
        verbose_name_plural = "Schools Attended"


class SSCEResult(models.Model):
    EXAM_TYPES = (
        ('waec', 'WAEC'),
        ('neco', 'NECO'),
        ('nabteb', 'NABTEB'),
        ('nbais', 'NBAIS'),
    )

    GRADES = (
        ('A1', 'A1'),
        ('B2', 'B2'),
        ('B3', 'B3'),
        ('C4', 'C4'),
        ('C5', 'C5'),
        ('C6', 'C6'),
        ('D7', 'D7'),
        ('E8', 'E8'),
        ('F9', 'F9'),
    )

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='ssce_results')
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, blank=True)
    exam_number = models.CharField(max_length=50, blank=True)
    centre_number = models.CharField(max_length=50, blank=True)
    centre_name = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=4, blank=True)
    awaiting_result = models.BooleanField(default=False)

    english = models.CharField(max_length=2, choices=GRADES, blank=True)
    mathematics = models.CharField(max_length=2, choices=GRADES, blank=True)
    biology = models.CharField(max_length=2, choices=GRADES, blank=True)
    chemistry = models.CharField(max_length=2, choices=GRADES, blank=True)
    physics = models.CharField(max_length=2, choices=GRADES, blank=True)

    subject_6 = models.CharField(max_length=100, blank=True)
    grade_6 = models.CharField(max_length=2, choices=GRADES, blank=True)

    subject_7 = models.CharField(max_length=100, blank=True)
    grade_7 = models.CharField(max_length=2, choices=GRADES, blank=True)

    subject_8 = models.CharField(max_length=100, blank=True)
    grade_8 = models.CharField(max_length=2, choices=GRADES, blank=True)

    subject_9 = models.CharField(max_length=100, blank=True)
    grade_9 = models.CharField(max_length=2, choices=GRADES, blank=True)

    def __str__(self):
        return f"{self.exam_type} - {self.year}"

    class Meta:
        verbose_name = "SSCE Result"
        verbose_name_plural = "SSCE Results"


class UploadedDocument(models.Model):
    DOCUMENT_TYPES = (
        ('ssce', 'SSCE Results'),
        ('primary', 'Primary School Certificate'),
        ('indigene', 'Indigene Certificate'),
        ('birth', 'Birth Certificate/Declaration of Age'),
        ('other', 'Other Credentials'),
    )

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application.application_number} - {self.get_document_type_display()}"

    class Meta:
        verbose_name = "Uploaded Document"
        verbose_name_plural = "Uploaded Documents"
