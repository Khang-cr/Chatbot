# Mental Health Counseling Chatbot

A Django-based web application for student mental health assessment using DASS-21 (Depression, Anxiety and Stress Scale).

## Features

- User registration and authentication
- DASS-21 mental health assessment (21 questions)
- Automatic scoring and level classification
- Personalized recommendations based on results
- Assessment history tracking
- User profile management

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

**Windows:**
```bash
venv\Scripts\activate
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
python manage.py migrate
```

### 6. Create superuser
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## DASS-21 Assessment

The DASS-21 measures three related states:
- **Depression** (7 items)
- **Anxiety** (7 items)  
- **Stress** (7 items)

Each item is scored from 0-3, and scores are classified into severity levels:
- Normal
- Mild
- Moderate
- Severe
- Extremely Severe

## Project Structure

```
Chatbot/
├── accounts/              # User authentication and profiles
├── chatbot_project/       # Project settings
├── templates/             # HTML templates
│   └── registration/      # Auth and assessment templates
├── venv/                  # Virtual environment (not in git)
├── db.sqlite3            # Database (not in git)
├── manage.py
└── requirements.txt
```

## Technologies Used

- Python 3.11
- Django 5.2.8

## License

This project is for educational purposes.

