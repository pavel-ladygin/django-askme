from django.core.management.base import BaseCommand
import time


class Command(BaseCommand):
    help = "Команда для заполнения БД данными"

    def handle(self, *args, **kwargs):
        self.stdout.write("Заполнение базы данных данными...")
        # Логика заполнения БД данными
        time.sleep(1)
        self.stdout.write("База данных успешно заполнена.")