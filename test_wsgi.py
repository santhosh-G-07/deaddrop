#!/usr/bin/env python
"""Simple test to see if WSGI application loads"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deaddrop.settings')
django.setup()

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("✅ WSGI application loaded successfully!")
    print(f"Application: {application}")
    
    # Try to start server manually
    print("\nNow trying to start development server...")
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000', '--noreload'])
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
