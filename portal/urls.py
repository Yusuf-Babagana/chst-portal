from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('referral-check/', views.referral_check, name='referral_check'),
    path('payment/', views.payment, name='payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('application/section-a/', views.section_a, name='section_a'),
    path('application/section-b/', views.section_b, name='section_b'),
    path('application/section-c/', views.section_c, name='section_c'),
    path('application/section-d/', views.section_d, name='section_d'),
    path('application/section-e/', views.section_e, name='section_e'),
    path('application/summary/', views.application_summary, name='application_summary'),
    path('application/download-pdf/', views.download_pdf, name='download_pdf'),
]
