import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facturacion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.test.utils import setup_test_environment

# Create a test user
user, created = User.objects.get_or_create(username='testuser')
if created:
    user.set_password('testpass')
    user.is_staff = True
    user.is_superuser = True
    user.save()

# Create test client and login
client = Client()
client.login(username='testuser', password='testpass')

# Get the dashboard
response = client.get('/', HTTP_HOST='127.0.0.1:8000')
print(f"Response status: {response.status_code}")

if response.status_code == 200:
    content = response.content.decode()
    
    # Find the rawMonthData section
    start = content.find("const rawMonthData = [")
    end = content.find("];", start) + 2
    
    if start != -1:
        data_section = content[start:end]
        print("\n=== Raw Month Data en HTML ===")
        print(data_section[:500])
        print("...")
