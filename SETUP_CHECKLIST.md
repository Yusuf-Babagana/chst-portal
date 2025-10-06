# CHSTH Admission Portal - Setup Checklist

## Pre-Deployment Checklist

### 1. Environment Setup
- [ ] Python 3.8+ installed
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)

### 2. Configuration
- [ ] `.env` file created from `.env.example`
- [ ] `SECRET_KEY` set in `.env`
- [ ] `PAYSTACK_PUBLIC_KEY` obtained and set
- [ ] `PAYSTACK_SECRET_KEY` obtained and set
- [ ] `DEBUG` set to `True` for development, `False` for production
- [ ] `ALLOWED_HOSTS` updated for production domain

### 3. Database Setup
- [ ] Migrations created (`python manage.py makemigrations`)
- [ ] Migrations applied (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Test login to admin panel successful

### 4. Referral Codes
- [ ] Referral codes generated (`python manage.py generate_referral_codes --count 100`)
- [ ] Referral codes verified in admin panel

### 5. File Structure
- [ ] `static/` directory created
- [ ] `media/` directory created
- [ ] `media/passports/` directory created
- [ ] `media/documents/` directory created
- [ ] Static files collected (`python manage.py collectstatic`)

### 6. Testing (Local)
- [ ] Development server runs (`python manage.py runserver`)
- [ ] Homepage loads successfully
- [ ] Signup process works
- [ ] Login process works
- [ ] Referral code application works
- [ ] Payment page loads (test mode)
- [ ] Application form sections load
- [ ] File uploads work
- [ ] Application submission works
- [ ] PDF download works
- [ ] Admin panel accessible
- [ ] Admin can view applications
- [ ] Admin can approve/reject applications

### 7. Paystack Integration
- [ ] Paystack account created
- [ ] Business details submitted (for live keys)
- [ ] Test keys obtained
- [ ] Test payment successful
- [ ] Payment callback working
- [ ] Payment records in database
- [ ] Live keys obtained (for production)

### 8. Production Deployment (PythonAnywhere)
- [ ] PythonAnywhere account created
- [ ] Project files uploaded
- [ ] Virtual environment created on server
- [ ] Dependencies installed on server
- [ ] Migrations run on server
- [ ] Superuser created on server
- [ ] Referral codes generated on server
- [ ] WSGI file configured
- [ ] Virtual environment path set
- [ ] Static files mapping configured
- [ ] Media files mapping configured
- [ ] Static files collected on server
- [ ] `DEBUG = False` in production settings
- [ ] `ALLOWED_HOSTS` updated for domain
- [ ] Environment variables set
- [ ] Web app reloaded
- [ ] Production site accessible

### 9. Post-Deployment Testing
- [ ] Homepage loads on production
- [ ] Signup works on production
- [ ] Login works on production
- [ ] Referral codes work on production
- [ ] Payment integration works on production
- [ ] File uploads work on production
- [ ] Application submission works on production
- [ ] PDF download works on production
- [ ] Admin panel accessible on production
- [ ] All pages mobile-responsive
- [ ] SSL/HTTPS working

### 10. Security
- [ ] `SECRET_KEY` is strong and unique
- [ ] Secret keys not in version control
- [ ] `.gitignore` configured properly
- [ ] `DEBUG = False` in production
- [ ] Strong admin password set
- [ ] File upload security tested
- [ ] CSRF protection working
- [ ] SQL injection protection verified

### 11. Customization
- [ ] School branding updated in templates
- [ ] School colors configured
- [ ] Admin panel branding updated
- [ ] Application fee amount verified
- [ ] Course list verified and updated
- [ ] Email settings configured (optional)

### 12. Backup Strategy
- [ ] Database backup method established
- [ ] Media files backup method established
- [ ] Backup schedule created
- [ ] Restoration process tested

### 13. Documentation
- [ ] README.md reviewed
- [ ] DEPLOYMENT_GUIDE.md reviewed
- [ ] Admin credentials documented securely
- [ ] Paystack credentials documented securely
- [ ] Support contact information updated

### 14. Training
- [ ] Admin staff trained on portal usage
- [ ] Admin staff trained on application review
- [ ] Support process established
- [ ] FAQ created for students (optional)

### 15. Launch
- [ ] Announcement prepared
- [ ] Launch date set
- [ ] Support team ready
- [ ] Monitoring in place
- [ ] Emergency contact established

## Post-Launch Monitoring

### Daily Tasks
- [ ] Check for new applications
- [ ] Review payment transactions
- [ ] Monitor error logs
- [ ] Respond to support queries

### Weekly Tasks
- [ ] Review referral code usage
- [ ] Export application data
- [ ] Check system performance
- [ ] Update statistics

### Monthly Tasks
- [ ] Database backup
- [ ] Review and approve applications
- [ ] Generate reports
- [ ] Update dependencies
- [ ] Security audit

---

## Quick Start Commands

```bash
# Local Development
python manage.py runserver

# Create Admin
python manage.py createsuperuser

# Generate Referral Codes
python manage.py generate_referral_codes --count 100

# Collect Static Files
python manage.py collectstatic

# Run Migrations
python manage.py makemigrations
python manage.py migrate

# Backup Database
python manage.py dumpdata > backup.json

# Restore Database
python manage.py loaddata backup.json
```

---

## Emergency Contacts

**Technical Support:**
- Developer: [Contact Info]
- Hosting: support@pythonanywhere.com
- Payment: support@paystack.com

**System Admin:**
- Admin Username: [Set during setup]
- Admin Email: [Set during setup]

---

**Note:** Check off items as you complete them. Keep this checklist for reference during setup and maintenance.
