# CHSTH Admission Portal

A complete Django-based admission portal for the College of Health Sciences and Technology Hadejia (CHSTH).

## Features

- Student registration and authentication
- Referral code system (100+ unique codes)
- Paystack payment integration (₦7,500 application fee)
- Multi-step application form (Sections A-E)
- Auto-progressive form workflow
- Document upload functionality
- PDF generation for completed applications
- Comprehensive Django Admin panel
- Mobile-responsive Bootstrap 4 design
- SQLite database (PythonAnywhere ready)

## Installation

### 1. Clone or Download the Project

```bash
cd django_app
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update with your settings:

```bash
cp .env.example .env
```

Edit `.env` and add your Paystack keys:
```
SECRET_KEY=your-django-secret-key
DEBUG=True
PAYSTACK_PUBLIC_KEY=pk_test_your_public_key
PAYSTACK_SECRET_KEY=sk_test_your_secret_key
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Generate Referral Codes

Generate 100 referral codes:

```bash
python manage.py generate_referral_codes --count 100
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 8. Create Static and Media Directories

```bash
mkdir static
mkdir media
mkdir media/passports
mkdir media/documents
```

### 9. Collect Static Files

```bash
python manage.py collectstatic
```

### 10. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the portal.

## Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin` using your superuser credentials.

### Admin Features:

- View and manage all students
- View and manage all applications
- Approve/Reject applications
- Export applications to CSV
- View all payments and transactions
- Manage referral codes
- View referral code usage

## Application Flow

1. **Student Signs Up** - Creates account with email and password
2. **Referral Code or Payment** - Either enter referral code or pay ₦7,500
3. **Section A** - Personal information and guardian details
4. **Section B** - Schools attended (up to 3)
5. **Section C** - SSCE results (up to 2 sittings)
6. **Section D** - Course selection (first and second choice)
7. **Section E** - Declaration and document upload
8. **Submit** - Application is submitted and can be downloaded as PDF

## Available Courses

- Diploma in Community Health (SCHEW)
- Certificate in Community Health (JCHEW)
- Diploma in Health Information Management
- Diploma in Environmental Health
- Diploma in X-Ray and Imaging
- Diploma in Nutrition and Dietetics
- Retraining in Community Health (JCHEW holders)

## Deployment to PythonAnywhere

### 1. Upload Files

Upload your project to PythonAnywhere using git or the Files interface.

### 2. Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 chsth_env
pip install -r requirements.txt
```

### 3. Configure Web App

- Go to Web tab
- Add a new web app
- Choose Manual configuration (Python 3.10)
- Set source code directory: `/home/yourusername/django_app`
- Set working directory: `/home/yourusername/django_app`

### 4. Configure WSGI File

Edit the WSGI configuration file:

```python
import os
import sys

path = '/home/yourusername/django_app'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'chsth_admission.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 5. Set Environment Variables

In the Web tab, add your environment variables:
- SECRET_KEY
- PAYSTACK_PUBLIC_KEY
- PAYSTACK_SECRET_KEY

### 6. Configure Static Files

In the Web tab, add static file mappings:
- URL: `/static/`
- Directory: `/home/yourusername/django_app/staticfiles/`

- URL: `/media/`
- Directory: `/home/yourusername/django_app/media/`

### 7. Update Settings for Production

In `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
SECRET_KEY = os.environ.get('SECRET_KEY')
```

### 8. Run Migrations and Setup

```bash
cd ~/django_app
workon chsth_env
python manage.py migrate
python manage.py createsuperuser
python manage.py generate_referral_codes --count 100
python manage.py collectstatic
```

### 9. Reload Web App

Click the "Reload" button on the Web tab.

## Paystack Integration

### Get Paystack Keys

1. Sign up at https://paystack.com
2. Go to Settings > API Keys & Webhooks
3. Copy your Public Key and Secret Key
4. Add them to your `.env` file or environment variables

### Test Mode

Use test keys (starting with `pk_test_` and `sk_test_`) for development.

### Live Mode

Use live keys (starting with `pk_live_` and `sk_live_`) for production.

## Customization

### Change School Name or Branding

Edit `chsth_admission/urls.py`:

```python
admin.site.site_header = "Your School Name"
admin.site.site_title = "Your School Admin"
```

### Change Colors

Edit `templates/base.html` CSS variables:

```css
:root {
    --primary-color: #1a5490;
    --secondary-color: #2c7abf;
}
```

### Change Application Fee

Edit `chsth_admission/settings.py`:

```python
APPLICATION_FEE = 7500  # Change to your amount
```

## Troubleshooting

### Static Files Not Loading

```bash
python manage.py collectstatic --clear
```

### Database Errors

```bash
python manage.py makemigrations
python manage.py migrate
```

### Permission Errors on Media Files

Make sure media directories are writable:

```bash
chmod -R 755 media/
```

## Support

For questions or issues, contact the development team.

## License

Copyright © 2025 College of Health Sciences and Technology Hadejia
