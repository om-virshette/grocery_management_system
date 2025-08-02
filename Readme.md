# Grocery Management System

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Django](https://img.shields.io/badge/django-4.2-brightgreen)
![DRF](https://img.shields.io/badge/drf-3.14-blueviolet)

A full-featured Django web application for managing grocery store operations including inventory, orders, reporting, and user management.

## Features

### Core Modules
- **Product Management**
  - CRUD operations for products
  - Barcode generation/scanning
  - Inventory tracking with stock alerts
  - Category management

- **Order Management**
  - Customer billing system
  - PDF invoice generation
  - Order status tracking (pending/completed/cancelled)
  - Stock auto-update on orders

- **User Authentication**
  - Custom user model with roles (admin/staff)
  - Registration and login system
  - Profile management
  - Staff management interface

- **Reporting System**
  - Sales reports with time filters
  - Inventory status reports
  - Product performance analytics
  - Low stock/out of stock alerts

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL (recommended) or SQLite
- Redis (for caching, optional)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/om-virshette/grocery-management-system.git
   cd grocery-management-system
Create and activate virtual environment:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Install dependencies:

bash
pip install -r requirements.txt
Configure environment variables:

bash
cp .env.example .env
Edit .env with your database credentials and secret key.

Run migrations:

bash
python manage.py migrate
Create superuser:

bash
python manage.py createsuperuser
Run development server:

bash
python manage.py runserver
Project Structure
text
grocery_management/
├── grocery_management/          # Main project config
├── products/                    # Product management
├── orders/                      # Order processing
├── users/                       # Authentication system
├── reports/                     # Reporting module
├── static/                      # Static files
├── templates/                   # HTML templates
├── .env.example                 # Environment template
├── manage.py
└── requirements.txt
API Documentation
Access the interactive API docs at:

Configuration
Key settings in settings.py:

python
# Custom user model
AUTH_USER_MODEL = 'users.User'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# API Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
Deployment
For production deployment:

Configure production database in settings.py

Set DEBUG = False

Configure static files:

bash
python manage.py collectstatic
Use WSGI server (Gunicorn/Uvicorn)

Set up web server (Nginx/Apache)