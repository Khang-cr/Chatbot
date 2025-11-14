# Mental Health Counseling Chatbot

A Django-based web application for mental health assessment using DASS-21 (Depression, Anxiety and Stress Scale) with separate portals for students and therapists.

## Features

### For Students:
- User registration and authentication
- DASS-21 mental health assessment (21 questions)
- Automatic scoring and severity level classification
- Personalized recommendations based on results
- Assessment history tracking
- Profile management

### For Therapists:
- Professional verification system
- Access to verified therapist profiles
- Specialized mental health counseling features

## Technologies Used

- Python 3.11+
- Django 5.1+
- SQLite (development)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Chatbot.git
cd Chatbot
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

### 8. Access the application
Visit `http://127.0.0.1:8000/` in your browser.

## For Team Members

When pulling new changes:

```bash
git pull origin main
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## DASS-21 Assessment

The DASS-21 measures three related states:

| Category | Items | Score Range |
|----------|-------|-------------|
| Depression | 7 questions | 0-21 |
| Anxiety | 7 questions | 0-21 |
| Stress | 7 questions | 0-21 |

Severity levels: Normal, Mild, Moderate, Severe, Extremely Severe

Each item is scored from 0 (Did not apply to me at all) to 3 (Applied to me very much).

## Project Structure

```
Chatbot/
├── accounts/              # User authentication and profiles
│   ├── models.py         # User, UserProfile, DASS21Result models
│   ├── views.py          # Authentication and assessment views
│   ├── forms.py          # User forms
│   └── urls.py           # URL routing
├── chatbot_project/      # Project settings
│   ├── settings.py       # Django configuration
│   └── urls.py           # Main URL configuration
├── templates/            # HTML templates
│   └── registration/     # Auth and assessment pages
├── venv/                 # Virtual environment (not in git)
├── db.sqlite3           # Database (not in git)
├── manage.py
└── requirements.txt
```

## Common Issues

**Error: "no such table: auth_user"**
- Run: `python manage.py migrate`

**Cannot activate venv on PowerShell**
- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Port 8000 already in use**
- Run: `python manage.py runserver 8080`

## License

This project is for educational purposes.
