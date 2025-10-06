from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Student, Application, Payment, ReferralCode, SchoolAttended, SSCEResult, UploadedDocument
from .forms import (
    SignupForm, LoginForm, ReferralCodeForm, SectionAForm,
    SchoolAttendedFormSet, SSCEResultFormSet, SectionDForm,
    SectionEForm, DocumentUploadFormSet
)
import requests
import json
from django.utils import timezone


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'portal/home.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user, phone=form.cleaned_data.get('phone'))
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('referral_check')
    else:
        form = SignupForm()

    return render(request, 'portal/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'portal/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


@login_required
def referral_check(request):
    student = request.user.student

    if student.has_paid or student.used_referral:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ReferralCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code:
                try:
                    referral = ReferralCode.objects.get(code=code, is_used=False)
                    referral.is_used = True
                    referral.used_by = request.user
                    referral.used_at = timezone.now()
                    referral.save()

                    student.used_referral = True
                    student.referral_code = referral
                    student.save()

                    messages.success(request, 'Referral code applied successfully! You can now proceed.')
                    return redirect('dashboard')
                except ReferralCode.DoesNotExist:
                    messages.error(request, 'Invalid or already used referral code.')
            else:
                return redirect('payment')
    else:
        form = ReferralCodeForm()

    return render(request, 'portal/referral_check.html', {'form': form})


@login_required
def payment(request):
    student = request.user.student

    if student.has_paid or student.used_referral:
        return redirect('dashboard')

    reference = f"CHSTH-{request.user.id}-{timezone.now().timestamp()}"

    Payment.objects.create(
        student=student,
        reference=reference,
        amount=settings.APPLICATION_FEE,
        status='pending'
    )

    context = {
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        'email': request.user.email,
        'amount': settings.APPLICATION_FEE * 100,
        'reference': reference,
    }

    return render(request, 'portal/payment.html', context)


@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reference = data.get('reference')

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'
        }

        response = requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers=headers
        )

        if response.status_code == 200:
            response_data = response.json()
            if response_data['data']['status'] == 'success':
                try:
                    payment = Payment.objects.get(reference=reference)
                    payment.status = 'success'
                    payment.paystack_reference = response_data['data']['reference']
                    payment.save()

                    student = payment.student
                    student.has_paid = True
                    student.save()

                    return JsonResponse({'status': 'success'})
                except Payment.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Payment not found'})

        return JsonResponse({'status': 'error', 'message': 'Payment verification failed'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def dashboard(request):
    student = request.user.student

    if not (student.has_paid or student.used_referral):
        return redirect('referral_check')

    try:
        application = student.application
    except Application.DoesNotExist:
        application = Application.objects.create(student=student)

    context = {
        'application': application,
        'student': student,
    }

    return render(request, 'portal/dashboard.html', context)


@login_required
def section_a(request):
    student = request.user.student

    if not (student.has_paid or student.used_referral):
        return redirect('referral_check')

    try:
        application = student.application
    except Application.DoesNotExist:
        application = Application.objects.create(student=student)

    if request.method == 'POST':
        form = SectionAForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            application.section_a_completed = True
            application.save()
            messages.success(request, 'Section A saved successfully!')
            return redirect('section_b')
    else:
        form = SectionAForm(instance=application)

    return render(request, 'portal/section_a.html', {'form': form, 'application': application})


@login_required
def section_b(request):
    student = request.user.student

    if not (student.has_paid or student.used_referral):
        return redirect('referral_check')

    try:
        application = student.application
    except Application.DoesNotExist:
        return redirect('section_a')

    if request.method == 'POST':
        formset = SchoolAttendedFormSet(request.POST, instance=application)
        if formset.is_valid():
            formset.save()
            application.section_b_completed = True
            application.save()
            messages.success(request, 'Section B saved successfully!')
            return redirect('section_c')
    else:
        formset = SchoolAttendedFormSet(instance=application)

    return render(request, 'portal/section_b.html', {'formset': formset, 'application': application})


@login_required
def section_c(request):
    student = request.user.student

    if not (student.has_paid or student.used_referral):
        return redirect('referral_check')

    try:
        application = student.application
    except Application.DoesNotExist:
        return redirect('section_a')

    if request.method == 'POST':
        formset = SSCEResultFormSet(request.POST, instance=application)
        if formset.is_valid():
            formset.save()
            application.section_c_completed = True
            application.save()
            messages.success(request, 'Section C saved successfully!')
            return redirect('section_d')
    else:
        formset = SSCEResultFormSet(instance=application)

    return render(request, 'portal/section_c.html', {'formset': formset, 'application': application})


@login_required
def section_d(request):
    student = request.user.student

    if not (student.has_paid or student.used_referral):
        return redirect('referral_check')

    try:
        application = student.application
    except Application.DoesNotExist:
        return redirect('section_a')

    if request.method == 'POST':
        form = SectionDForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            application.section_d_completed = True
            application.save()
            messages.success(request, 'Section D saved successfully!')
            return redirect('section_e')
    else:
        form = SectionDForm(instance=application)

    return render(request, 'portal/section_d.html', {'form': form, 'application': application})


@login_required
def section_e(request):
    student = request.user.student

    if not (student.has_paid or student.used_referral):
        return redirect('referral_check')

    try:
        application = student.application
    except Application.DoesNotExist:
        return redirect('section_a')

    if request.method == 'POST':
        form = SectionEForm(request.POST, instance=application)
        formset = DocumentUploadFormSet(request.POST, request.FILES, instance=application)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            application.section_e_completed = True
            application.status = 'submitted'
            application.submitted_at = timezone.now()
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('application_summary')
    else:
        form = SectionEForm(instance=application)
        formset = DocumentUploadFormSet(instance=application)

    return render(request, 'portal/section_e.html', {
        'form': form,
        'formset': formset,
        'application': application
    })


@login_required
def application_summary(request):
    student = request.user.student

    try:
        application = student.application
    except Application.DoesNotExist:
        return redirect('dashboard')

    context = {
        'application': application,
        'schools': application.schools_attended.all(),
        'results': application.ssce_results.all(),
        'documents': application.documents.all(),
    }

    return render(request, 'portal/application_summary.html', context)


@login_required
def download_pdf(request):
    from .utils import generate_application_pdf

    student = request.user.student

    try:
        application = student.application
    except Application.DoesNotExist:
        messages.error(request, 'No application found.')
        return redirect('dashboard')

    pdf = generate_application_pdf(application)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{application.application_number}.pdf"'

    return response
