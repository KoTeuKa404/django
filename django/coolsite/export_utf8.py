import sys
from django.core.management import call_command
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coolsite.settings")  
django.setup()
try:
    with open("all_data.json", "w", encoding="utf-8") as f:
        call_command("dumpdata", indent=2, stdout=f)
except Exception as e:
    print(f"Помилка експорту: {e}")