# CertiChain — Bash Commands Reference

All commands for managing the CertiChain platform on PythonAnywhere.

---

## 🔧 Server Setup (First Time)

```bash
# Clone the repository
git clone https://github.com/sahilansari189/certichain.git
cd certichain

# Create virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies
pip install -r lms/requirements.txt

# Set up the database
cd lms
python manage.py migrate
python manage.py createsuperuser

# Seed demo courses
python manage.py seed_courses

# Collect static files
python manage.py collectstatic --noinput
```

---

## 🔄 Deployment (After Code Changes)

```bash
# Navigate to project
cd ~/certichain

# Pull latest changes
git pull origin main

# Activate virtual environment
source env/bin/activate

# Install any new dependencies
pip install -r lms/requirements.txt

# Run migrations (if any)
cd lms
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

> **Important:** After pulling, go to the PythonAnywhere **Web** tab and click **Reload** to apply changes.

---

## 📚 Course Management

```bash
# Seed all demo courses (Code Blocks, Blockchain Mastery, Web Dev Bootcamp)
python manage.py seed_courses

# Open Django shell to manage data
python manage.py shell

# Delete all courses (in Django shell)
# from course.models import Course
# Course.objects.all().delete()

# Delete specific course (in Django shell)
# Course.objects.filter(slug='web-development-bootcamp').delete()
```

---

## 👤 User Management

```bash
# Create a superuser
python manage.py createsuperuser

# Change a user's password
python manage.py changepassword <username>

# Open Django admin
# Visit: https://sahilansari189.pythonanywhere.com/admin/
```

---

## 🗄️ Database

```bash
# Run all pending migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Show migration status
python manage.py showmigrations

# Reset database (CAUTION: deletes all data)
rm lms/db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_courses
```

---

## 📦 Dependencies

```bash
# Install all requirements
pip install -r lms/requirements.txt

# Add a new package
pip install <package-name>
pip freeze > lms/requirements.txt

# Check installed packages
pip list
```

---

## 🔍 Debugging

```bash
# Check error logs on PythonAnywhere
cat /var/log/sahilansari189.pythonanywhere.com.error.log

# Tail logs in real-time
tail -f /var/log/sahilansari189.pythonanywhere.com.error.log

# Test email sending
cd lms
python manage.py shell
# from django.core.mail import send_mail
# from django.conf import settings
# send_mail('Test', 'Test email body', settings.EMAIL_HOST_USER, ['your@email.com'])

# Run development server locally
python manage.py runserver
```

---

## 🌐 Git Commands

```bash
# Check status
git status

# Stage all changes
git add .

# Commit changes
git commit -m "your message"

# Push to GitHub
git push origin main

# Pull from GitHub
git pull origin main

# View recent commits
git log -n 5 --oneline

# Discard local changes
git checkout -- .

# Reset to remote
git fetch origin
git reset --hard origin/main
```

---

## 🔐 Environment Variables

Required `.env` variables in `lms/.env`:

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost,sahilansari189.pythonanywhere.com

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

EMAILJS_SERVICE_ID=your-service-id
EMAILJS_TEMPLATE_ID=your-template-id
EMAILJS_PUBLIC_KEY=your-public-key
IMGBB_KEY=your-imgbb-key
```

---

## ⚡ Quick Deploy (One-Liner)

```bash
cd ~/certichain && git pull origin main && source env/bin/activate && cd lms && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && echo "✅ Done! Reload from Web tab."
```

---

**CertiChain** — Blockchain-Powered Learning & Certification
