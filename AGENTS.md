# AGENTS.md - covid_vis Development Guide

This document provides guidelines for agents working on the covid_vis codebase.

## Project Overview

covid_vis is a Django 5.x web application for managing COVID-19 hospital data in Chikkamagaluru. It tracks hospitals, patients, beds, and vaccination status.

## Build / Lint / Test Commands

### Local Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

### Database Migrations
```bash
python manage.py makemigrations  # Create migrations
python manage.py migrate         # Apply migrations
python manage.py createsuperuser # Create admin user
```

### Running Tests
```bash
# Run all tests
python manage.py test

# Run a single test app
python manage.py test covid_vis.core

# Run a specific test class/method (Django 4.2+)
python manage.py test covid_vis.core.tests --keepdb

# Run with verbose output
python manage.py test -v 2
```

### Code Formatting & Linting
```bash
# Format all Python files (uses Black profile)
isort .

# Check import sorting
isort --check-only --diff .

# Lint all Python files
flake8 .

# Format with Black (trunk tool)
black .
```

### Using Trunk (recommended)
```bash
trunk check    # Run all linters
trunk fmt      # Format all files
```

### Production Server
```bash
gunicorn covid_vis.wsgi --bind 0.0.0.0:8000
```

## Code Style Guidelines

### General Principles
- Follows Django best practices and PEP 8
- Uses Black for code formatting (isort profile: black)
- Uses flake8 with relaxed settings (ignores D1, D2, E1, E2, E3, E501, W1, W2, W3, W5)
- No trailing whitespace or unnecessary blank lines

### Python Version
- Target: Python 3.10+ (runtime.txt specifies python-3.10.7)

### Django Conventions

#### Models (`covid_vis/core/models.py`)
- Use docstrings for model classes: `"""Model Name"""`
- Define `__str__` method on all models returning `f"{self.name}"`
- Use verbose_name for admin-displayed field names
- Use `auto_now_add` for creation timestamps, `auto_now` for updates
- Use `on_delete=models.CASCADE` or `on_delete=models.DO_NOTHING` explicitly
- Phone fields: use `PhoneNumberField` from `phonenumber_field`

#### Views (`covid_vis/core/views.py`)
- Use function-based views for simple pages
- Use class-based views (SingleTableMixin, FilterView) for list pages
- Always return `render(request, "template.html", context)` or raise Http404
- Use `get_object_or_404` for single-object lookups

#### Admin (`covid_vis/core/admin.py`)
- Register models with custom ModelAdmin classes for business logic
- Filter querysets by user: `qs.filter(created_by=request.user)` for non-superusers
- Set `exclude` tuples for auto-computed fields

#### Templates
- Template location: `covid_vis/core/templates/`
- Use Bootstrap 4 template (`django_tables2/bootstrap4.html`)
- Use `{% extends "base.html" %}` pattern

### Import Organization
- Standard library imports first
- Third-party imports second
- Local imports last
- Use `isort` with Black profile for automatic sorting
- Example:
  ```python
  import datetime

  import django_tables2 as tables
  from django.db.models import Count, Q, Sum
  from django.shortcuts import render

  from .models import Hospital, Patient
  ```

### Naming Conventions
- Models: PascalCase (e.g., `Hospital`, `Patient`)
- Model fields: snake_case (e.g., `hospital_admin`, `beds_available`)
- View functions: snake_case (e.g., `hospital_detail`, `graphs`)
- URLs: snake_case names (e.g., `hospital_detail`)
- Template files: snake_case (e.g., `hospital_list.html`)
- Constants/Choices: UPPER_SNAKE_CASE for choice tuples

### Error Handling
- Use Django's `get_object_or_404` for 404 responses
- Use `try/except` sparingly; prefer Django's view shortcuts
- Database operations: rely on Django ORM; avoid raw SQL unless necessary

### Database
- Default: SQLite (development); PostgreSQL via env vars (production)
- Use Django migrations for all schema changes
- Configure via environment variables:
  - `DB_ENGINE`: database backend
  - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

### Settings (`covid_vis/settings.py`)
- Use `django-environ` for environment variables
- Default SECRET_KEY is insecure; always override in production
- DEBUG defaults to True; set `DEBUG=False` in production
- ALLOWED_HOSTS defaults to localhost/127.0.0.1/0.0.0.0

### Dependencies
- Django 5.1.x
- django-tables2, django-filter for list views
- phonenumber-field for phone validation
- beautifulsoup4, soupsieve for HTML parsing
- gunicorn for production server
- whitenoise for static file serving
- See `requirements.txt` for full list

### Key Files
- `manage.py`: Django management script
- `covid_vis/settings.py`: Configuration
- `covid_vis/urls.py`: URL routing
- `covid_vis/core/models.py`: Database models
- `covid_vis/core/views.py`: View functions
- `covid_vis/core/admin.py`: Admin configuration
- `covid_vis/core/tests.py`: Tests (currently empty)
- `.trunk/trunk.yaml`: Trunk linter configuration
- `.flake8`: Flake8 configuration
- `.isort.cfg`: isort configuration
