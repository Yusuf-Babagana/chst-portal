from django.contrib import admin
from django.utils.html import format_html
from .models import Student, Application, Payment, ReferralCode, SchoolAttended, SSCEResult, UploadedDocument


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'has_paid', 'used_referral', 'created_at']
    list_filter = ['has_paid', 'used_referral', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'status', 'reference', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['student__user__username', 'student__user__email', 'reference', 'paystack_reference']
    readonly_fields = ['created_at', 'updated_at']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'is_used', 'used_by', 'used_at', 'created_at']
    list_filter = ['is_used', 'created_at', 'used_at']
    search_fields = ['code', 'used_by__username', 'used_by__email']
    readonly_fields = ['used_by', 'used_at', 'created_at']

    def has_add_permission(self, request):
        return True


class SchoolAttendedInline(admin.TabularInline):
    model = SchoolAttended
    extra = 0


class SSCEResultInline(admin.TabularInline):
    model = SSCEResult
    extra = 0


class UploadedDocumentInline(admin.TabularInline):
    model = UploadedDocument
    extra = 0
    readonly_fields = ['uploaded_at']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'application_number', 'student_name', 'email', 'first_choice',
        'status', 'progress', 'submitted_at'
    ]
    list_filter = ['status', 'first_choice', 'submitted_at', 'created_at']
    search_fields = [
        'application_number', 'student__user__username', 'student__user__email',
        'first_name', 'surname', 'email'
    ]
    readonly_fields = ['application_number', 'created_at', 'updated_at', 'submitted_at']
    inlines = [SchoolAttendedInline, SSCEResultInline, UploadedDocumentInline]

    fieldsets = (
        ('Application Info', {
            'fields': ('application_number', 'student', 'status', 'submitted_at')
        }),
        ('Personal Information', {
            'fields': (
                'passport_photo', 'first_name', 'surname', 'other_names',
                'date_of_birth', 'phone', 'email', 'address', 'lga', 'state_of_origin'
            )
        }),
        ('Guardian/Next of Kin', {
            'fields': ('guardian_name', 'guardian_phone', 'guardian_address', 'guardian_relationship')
        }),
        ('Course Selection', {
            'fields': ('first_choice', 'second_choice')
        }),
        ('Declaration', {
            'fields': ('declaration_text',)
        }),
        ('Progress Tracking', {
            'fields': (
                'section_a_completed', 'section_b_completed', 'section_c_completed',
                'section_d_completed', 'section_e_completed'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student Name'

    def progress(self, obj):
        completed = sum([
            obj.section_a_completed,
            obj.section_b_completed,
            obj.section_c_completed,
            obj.section_d_completed,
            obj.section_e_completed
        ])
        total = 5
        percentage = (completed / total) * 100
        color = 'green' if percentage == 100 else 'orange' if percentage >= 50 else 'red'
        return format_html(
            '<span style="color: {};">{}/5 ({}%)</span>',
            color, completed, int(percentage)
        )
    progress.short_description = 'Progress'

    actions = ['approve_applications', 'reject_applications', 'export_to_csv']

    def approve_applications(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} application(s) approved successfully.')
    approve_applications.short_description = 'Approve selected applications'

    def reject_applications(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} application(s) rejected.')
    reject_applications.short_description = 'Reject selected applications'

    def export_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        import io

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="applications.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Application Number', 'Student Name', 'Email', 'Phone',
            'First Choice', 'Second Choice', 'Status', 'Submitted At'
        ])

        for application in queryset:
            writer.writerow([
                application.application_number,
                application.student.user.get_full_name(),
                application.email,
                application.phone,
                application.get_first_choice_display(),
                application.get_second_choice_display(),
                application.status,
                application.submitted_at
            ])

        return response
    export_to_csv.short_description = 'Export selected to CSV'


@admin.register(SchoolAttended)
class SchoolAttendedAdmin(admin.ModelAdmin):
    list_display = ['application', 'school_name', 'from_year', 'to_year']
    search_fields = ['application__application_number', 'school_name']


@admin.register(SSCEResult)
class SSCEResultAdmin(admin.ModelAdmin):
    list_display = ['application', 'exam_type', 'year', 'awaiting_result']
    list_filter = ['exam_type', 'year', 'awaiting_result']
    search_fields = ['application__application_number', 'exam_number']


@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ['application', 'document_type', 'document_file', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['application__application_number']
    readonly_fields = ['uploaded_at']
