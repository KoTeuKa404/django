# test_app/tasks.py
from celery import shared_task

@shared_task
def add(x, y):
    print(f"Додаю {x} + {y}")
    return x + y
