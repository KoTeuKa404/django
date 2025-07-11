# coolsite/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coolsite.settings')

app = Celery('coolsite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
