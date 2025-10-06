# CHSTH Admission Portal - Complete Deployment Guide

## Quick Start (Local Development)

```bash
# 1. Navigate to project directory
cd django_app

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Setup environment variables
cp .env.example .env
# Edit .env with your Paystack keys

# 6. Run migrations
python manage.py makemigrations
python manage.py migrate

# 7. Generate referral codes
python manage.py generate_referral_codes --count 100

# 8. Create admin user
python manage.py createsuperuser

# 9. Create directories
mkdir -p static media media/passports media/documents

# 10. Collect static files
python manage.py collectstatic --noinput

# 11. Run server
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

Admin: `http://127.0.0.1:8000/admin`

---

## PythonAnywhere Deployment (Detailed)

### Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Sign up for a free or paid account
3. Log in to your dashboard

### Step 2: Upload Project Files

**Option A: Using Git (Recommended)**

```bash
# In PythonAnywhere Bash console
git clone https://github.com/yourusername/chsth-admission.git
cd chsth-admission/django_app
```

**Option B: Using Files Tab**

1. Click "Files" tab
2. Create directory: `django_app`
3. Upload all project files using the upload button
4. Or use "Upload a file" to upload a zip file and extract it

### Step 3: Create Virtual Environment

In PythonAnywhere Bash console:

```bash
# Navigate to project
cd ~/django_app

# Create virtual environment (Python 3.10 recommended)
mkvirtualenv --python=/usr/bin/python3.10 chsth_env

# Activate environment (happens automatically after creation)
workon chsth_env

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Database

```bash
# Still in Bash console with activated environment
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser

```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### Step 6: Generate Referral Codes

```bash
python manage.py generate_referral_codes --count 100
```

### Step 7: Create Media Directories

```bash
mkdir -p media/passports media/documents
```

### Step 8: Setup Web App

1. Go to "Web" tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose your domain (e.g., `yourusername.pythonanywhere.com`)
4. Select "Manual configuration"
5. Choose "Python 3.10"

### Step 9: Configure WSGI File

1. In "Web" tab, click on WSGI configuration file link
2. Delete all content
3. Add this code (replace `yourusername` with your PythonAnywhere username):

```python
import os
import sys

# Add your project directory to sys.path
project_home = '/home/yourusername/django_app'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'chsth_admission.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. Click "Save"

### Step 10: Configure Virtual Environment Path

In "Web" tab:

1. Find "Virtualenv" section
2. Enter path: `/home/yourusername/.virtualenvs/chsth_env`
3. The path should turn blue/green if correct

### Step 11: Configure Static Files

In "Web" tab, scroll to "Static files" section:

Add two mappings:

**Mapping 1:**
- URL: `/static/`
- Directory: `/home/yourusername/django_app/staticfiles/`

**Mapping 2:**
- URL: `/media/`
- Directory: `/home/yourusername/django_app/media/`

### Step 12: Collect Static Files

```bash
# In Bash console
cd ~/django_app
workon chsth_env
python manage.py collectstatic --noinput
```

### Step 13: Update Django Settings for Production

Edit `chsth_admission/settings.py`:

```python
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# Paystack keys from environment
PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY', 'pk_test_xxxxxxxxxxxx')
PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY', 'sk_test_xxxxxxxxxxxx')
```

### Step 14: Set Environment Variables

**Option A: Using .env file**

```bash
# In Bash console
cd ~/django_app
nano .env
```

Add:
```
SECRET_KEY=your-super-secret-key-here
PAYSTACK_PUBLIC_KEY=pk_test_your_public_key
PAYSTACK_SECRET_KEY=sk_test_your_secret_key
```

Then install python-decouple:
```bash
pip install python-decouple
```

Update settings.py:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
PAYSTACK_PUBLIC_KEY = config('PAYSTACK_PUBLIC_KEY')
PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY')
```

**Option B: Using Environment Variables**

In PythonAnywhere, you can set environment variables but they need to be set in the WSGI file:

```python
# In WSGI file, before importing Django
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['PAYSTACK_PUBLIC_KEY'] = 'pk_test_xxx'
os.environ['PAYSTACK_SECRET_KEY'] = 'sk_test_xxx'
```

### Step 15: Reload Web App

1. In "Web" tab
2. Scroll to top
3. Click green "Reload yourusername.pythonanywhere.com" button

### Step 16: Test Your Site

1. Visit `https://yourusername.pythonanywhere.com`
2. Test signup, login, and application process
3. Test admin at `https://yourusername.pythonanywhere.com/admin`

---

## Getting Paystack API Keys

### Development/Test Keys

1. Go to https://paystack.com
2. Click "Get Started" or "Sign Up"
3. Complete registration
4. Verify your email
5. Log in to Dashboard
6. Go to Settings > API Keys & Webhooks
7. Copy "Test Public Key" (starts with `pk_test_`)
8. Copy "Test Secret Key" (starts with `sk_test_`)

### Production/Live Keys

1. Complete business verification on Paystack
2. Submit required documents
3. Wait for approval
4. Once approved, access "Live Keys" in Settings
5. Copy "Live Public Key" (starts with `pk_live_`)
6. Copy "Live Secret Key" (starts with `sk_live_`)

**Important:** Never commit your secret keys to version control!

---

## Troubleshooting

### Issue: "ImportError: No module named django"

**Solution:**
```bash
cd ~/django_app
workon chsth_env
pip install -r requirements.txt
```

Make sure virtualenv path is correct in Web tab.

### Issue: Static files not loading (CSS/JS missing)

**Solution:**
```bash
cd ~/django_app
workon chsth_env
python manage.py collectstatic --clear --noinput
```

Check static file mappings in Web tab are correct.

### Issue: "DisallowedHost" error

**Solution:**
Update `settings.py`:
```python
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'www.yourusername.pythonanywhere.com']
```

Reload web app.

### Issue: Database errors

**Solution:**
```bash
cd ~/django_app
workon chsth_env
python manage.py makemigrations
python manage.py migrate
```

### Issue: Media files not uploading

**Solution:**
```bash
cd ~/django_app
chmod -R 755 media/
```

Check media mapping in Web tab.

### Issue: "500 Internal Server Error"

**Solution:**
1. Check error log in Web tab
2. Set `DEBUG = True` temporarily in settings.py
3. Reload and check detailed error
4. Fix issue
5. Set `DEBUG = False` again
6. Reload

### Issue: Paystack payment not working

**Solution:**
1. Verify Paystack keys are correct
2. Check they're properly set in environment
3. Use test keys for testing
4. Check Paystack dashboard for transaction logs
5. Ensure callback URL is accessible

---

## Security Checklist

Before going live:

- [ ] Set `DEBUG = False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Add your domain to `ALLOWED_HOSTS`
- [ ] Never commit secret keys to Git
- [ ] Use environment variables for sensitive data
- [ ] Use HTTPS (PythonAnywhere provides this)
- [ ] Keep dependencies updated
- [ ] Regular backups of database
- [ ] Use strong admin password
- [ ] Restrict admin access if possible

---

## Maintenance

### Backup Database

```bash
cd ~/django_app
python manage.py dumpdata > backup_$(date +%Y%m%d).json
```

### Restore Database

```bash
python manage.py loaddata backup_20250101.json
```

### Update Code

```bash
cd ~/django_app
git pull origin main
workon chsth_env
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then reload web app.

### View Logs

PythonAnywhere Web tab:
- Error log: Shows Python errors
- Server log: Shows web server info
- Access log: Shows all requests

### Monitor Applications

Regularly check Django Admin:
- Review new applications
- Monitor payment transactions
- Check referral code usage
- Export data for reporting

---

## Custom Domain Setup (Optional)

### For Paid PythonAnywhere Accounts

1. Purchase domain from domain registrar
2. In PythonAnywhere Web tab, add domain
3. Configure DNS records at registrar:
   - Type: CNAME
   - Host: www
   - Value: webapp-XXXXX.pythonanywhere.com
   - Type: A
   - Host: @
   - Value: (IP provided by PythonAnywhere)
4. Wait for DNS propagation (can take 24-48 hours)
5. Update `ALLOWED_HOSTS` in settings.py
6. Reload web app

---

## Performance Optimization

### Database Optimization

Add indexes for frequently queried fields in `models.py`:

```python
class Application(models.Model):
    # ... existing fields ...

    class Meta:
        indexes = [
            models.Index(fields=['application_number']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]
```

Then run migrations.

### Caching (Advanced)

Install Redis cache:

```bash
pip install django-redis
```

Update settings.py:

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

---

## Support and Updates

For technical support or updates:
- Check Django documentation: https://docs.djangoproject.com
- Check PythonAnywhere help: https://help.pythonanywhere.com
- Check Paystack documentation: https://paystack.com/docs

---

**Congratulations! Your CHSTH Admission Portal is now deployed and ready to use.**
