import sys
from django.core.management import call_command
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coolsite.settings")
django.setup()

try:
    call_command("loaddata", "all_data.json")
    print("Дані успішно імпортовано з all_data.json")
except Exception as e:
    print(f"Помилка імпорту: {e}")
