import os
from horoscope_api.wsgi import application  # Import the WSGI application from your wsgi.py file

# Ensure that Django settings are properly configured for Vercel
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horoscope_api.settings')

# Vercel will use this `app` callable to process requests
app = application  # Add this line to explicitly assign the WSGI application to `app`

