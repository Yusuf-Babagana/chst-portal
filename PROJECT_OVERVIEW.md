# CHSTH Admission Portal - Project Overview

## Project Summary

A complete, production-ready Django web application for managing student admissions at the College of Health Sciences and Technology Hadejia (CHSTH).

## Key Features

### Student-Facing Features
1. **User Authentication**
   - Secure signup and login system
   - Password reset functionality
   - Session management

2. **Payment Options**
   - Paystack integration for ₦7,500 application fee
   - Referral code system to bypass payment
   - Transaction tracking and verification

3. **Multi-Section Application Form**
   - **Section A:** Personal information and guardian details
   - **Section B:** Educational history (up to 3 schools)
   - **Section C:** SSCE results (up to 2 sittings)
   - **Section D:** Course selection (first and second choice)
   - **Section E:** Declaration and document uploads

4. **Progressive Form Flow**
   - Auto-save functionality
   - Automatic progression between sections
   - Resume application anytime
   - Track completion progress

5. **Document Management**
   - Passport photo upload
   - Multiple document uploads (SSCE, certificates, etc.)
   - Secure file storage

6. **Application Review**
   - View submitted application
   - Download application as PDF
   - Print-friendly format

### Administrative Features

1. **Django Admin Panel**
   - Customized branding for CHSTH
   - Dashboard with statistics
   - Complete application management

2. **Student Management**
   - View all registered students
   - Track payment status
   - Monitor referral code usage

3. **Application Management**
   - View all applications
   - Filter by status, course, date
   - Approve or reject applications
   - Track application progress
   - Export to CSV/Excel

4. **Payment Tracking**
   - View all transactions
   - Verify payment status
   - Reconciliation tools

5. **Referral Code System**
   - Generate bulk referral codes
   - Track code usage
   - View which student used which code
   - Prevent duplicate usage

## Technical Stack

### Backend
- **Framework:** Django 4.2.7
- **Database:** SQLite3 (production-ready for small to medium scale)
- **Python Version:** 3.8+

### Frontend
- **CSS Framework:** Bootstrap 4.6
- **Icons:** Font Awesome 5
- **Forms:** django-crispy-forms with Bootstrap 4 theme
- **Responsive Design:** Mobile-first approach

### Third-Party Integrations
- **Payment Gateway:** Paystack
- **PDF Generation:** ReportLab
- **Image Processing:** Pillow
- **HTTP Requests:** Requests library

## Project Structure

```
django_app/
├── chsth_admission/          # Main project configuration
│   ├── __init__.py
│   ├── settings.py           # Project settings
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
│
├── portal/                   # Main application
│   ├── migrations/           # Database migrations
│   ├── management/           # Custom management commands
│   │   └── commands/
│   │       └── generate_referral_codes.py
│   ├── __init__.py
│   ├── admin.py             # Admin panel configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL patterns
│   ├── forms.py             # Form definitions
│   └── utils.py             # Utility functions (PDF generation)
│
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── portal/              # Portal templates
│       ├── home.html
│       ├── signup.html
│       ├── login.html
│       ├── referral_check.html
│       ├── payment.html
│       ├── dashboard.html
│       ├── section_a.html
│       ├── section_b.html
│       ├── section_c.html
│       ├── section_d.html
│       ├── section_e.html
│       └── application_summary.html
│
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   │   └── custom.css
│   └── js/
│       └── custom.js
│
├── media/                   # User uploaded files
│   ├── passports/           # Passport photos
│   └── documents/           # Application documents
│
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── README.md               # Main documentation
├── DEPLOYMENT_GUIDE.md     # Deployment instructions
├── SETUP_CHECKLIST.md      # Setup checklist
└── PROJECT_OVERVIEW.md     # This file
```

## Database Schema

### Models Overview

1. **User (Django built-in)**
   - username, email, password, first_name, last_name

2. **Student**
   - Extends User with phone and payment status
   - Links to User (OneToOne)
   - Tracks payment and referral status

3. **ReferralCode**
   - Unique codes for fee waiver
   - Usage tracking
   - Links to User who used it

4. **Payment**
   - Transaction records
   - Paystack reference
   - Status tracking
   - Links to Student

5. **Application**
   - Main application data
   - Personal information
   - Course selection
   - Section completion tracking
   - Links to Student (OneToOne)

6. **SchoolAttended**
   - Educational history
   - Multiple entries per application
   - Links to Application

7. **SSCEResult**
   - Exam results
   - Up to 2 sittings per application
   - Subject grades
   - Links to Application

8. **UploadedDocument**
   - Document metadata
   - File storage
   - Multiple per application
   - Links to Application

## Available Courses

1. Diploma in Community Health (SCHEW)
2. Certificate in Community Health (JCHEW)
3. Diploma in Health Information Management
4. Diploma in Environmental Health
5. Diploma in X-Ray and Imaging
6. Diploma in Nutrition and Dietetics
7. Retraining in Community Health (JCHEW holders)

## User Journey

### New Student Flow

1. **Landing Page**
   - View available programs
   - See application fee information
   - Choose to Sign Up or Login

2. **Sign Up**
   - Create account with email and password
   - Provide basic information
   - Auto-login after signup

3. **Referral Code or Payment**
   - Option 1: Enter referral code (if available)
   - Option 2: Proceed to payment
   - Cannot access forms without payment or valid code

4. **Payment (if no referral)**
   - Integrated Paystack payment
   - ₦7,500 application fee
   - Real-time verification
   - Transaction recorded

5. **Dashboard**
   - View application status
   - See progress for each section
   - Access forms
   - View submitted application (after submission)

6. **Complete Application**
   - Fill Section A (Personal Info)
   - Auto-progress to Section B (Schools)
   - Continue through C, D, E
   - Upload documents
   - Submit declaration

7. **Submit and Review**
   - Final submission
   - View complete application
   - Download PDF copy
   - Wait for admin review

### Admin Flow

1. **Login to Admin Panel**
   - Access at /admin
   - Use superuser credentials

2. **Dashboard**
   - View statistics
   - Recent applications
   - Payment summary

3. **Review Applications**
   - Filter by status/course/date
   - View complete application details
   - Review uploaded documents

4. **Take Action**
   - Approve application
   - Reject application
   - Export data for records

5. **Manage System**
   - Generate new referral codes
   - Monitor payments
   - View student data

## Security Features

1. **Authentication**
   - Password hashing (Django built-in)
   - Session management
   - CSRF protection

2. **Authorization**
   - Login required decorators
   - Permission-based access
   - Admin-only areas

3. **Data Protection**
   - SQL injection protection (Django ORM)
   - XSS protection
   - Secure file uploads

4. **Payment Security**
   - Paystack encryption
   - Transaction verification
   - Server-side validation

5. **Production Security**
   - DEBUG=False setting
   - Secret key protection
   - HTTPS enforcement

## Scalability Considerations

### Current Capacity
- SQLite can handle 10,000+ applications
- PythonAnywhere free tier: Good for testing
- PythonAnywhere paid tiers: Production-ready

### Future Scaling Options
1. **Database**
   - Migrate to PostgreSQL for larger scale
   - Add database indexing
   - Implement caching (Redis)

2. **File Storage**
   - Move to cloud storage (AWS S3, Azure)
   - CDN for static files

3. **Performance**
   - Add database connection pooling
   - Implement query optimization
   - Add load balancing

4. **Features**
   - Email notifications
   - SMS integration
   - Payment reminders
   - Application tracking
   - Analytics dashboard

## Customization Guide

### Branding
- Colors: Edit `templates/base.html` CSS variables
- Logo: Add to `static/images/` and update templates
- Text: Update templates and admin configuration

### Courses
- Edit `COURSES` choices in `portal/models.py`
- Run migrations after changes

### Application Fee
- Change `APPLICATION_FEE` in `settings.py`

### Form Fields
- Add/remove fields in `portal/models.py`
- Update corresponding forms in `portal/forms.py`
- Create and run migrations
- Update templates

## Maintenance Tasks

### Daily
- Check new applications
- Monitor payments
- Review error logs

### Weekly
- Export application data
- Backup database
- Review referral codes

### Monthly
- Update dependencies
- Security audit
- Generate reports

### As Needed
- Approve/reject applications
- Generate new referral codes
- Handle support requests

## Support Resources

### Documentation
- Django: https://docs.djangoproject.com
- Bootstrap: https://getbootstrap.com/docs/4.6
- Paystack: https://paystack.com/docs
- PythonAnywhere: https://help.pythonanywhere.com

### Community
- Django Forum: https://forum.djangoproject.com
- Stack Overflow: Tag [django]
- Paystack Support: support@paystack.com

## License

Copyright © 2025 College of Health Sciences and Technology Hadejia
All rights reserved.

## Credits

**Development Team:** Custom Django Application
**Framework:** Django Software Foundation
**Payment Gateway:** Paystack
**Hosting:** PythonAnywhere

---

**Version:** 1.0.0
**Last Updated:** 2025
**Status:** Production Ready
