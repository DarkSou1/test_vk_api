from django.core.management.base import BaseCommand

from ...servise import parse


class Command(BaseCommand):
    """Добавление своей команды."""
    help = 'Парсинг вк в базу данных'

    def handle(self, *args, **options):
        """Имрорт файла servise.py для парсинга вк."""
        parse()
