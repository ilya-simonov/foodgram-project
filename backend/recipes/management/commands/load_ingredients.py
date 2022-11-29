import json
import os

from django.core.management.base import BaseCommand

from foodgram.settings import BASE_DIR
from recipes.models import Ingredient

INGREDIENTS_JSON = 'ingredients.json'
# DATA_PATH = os.path.join(BASE_DIR, '..', 'data')
DATA_PATH = os.path.join(BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в БД из файла'

    def handle(self, *args, **options):
        path = os.path.join(DATA_PATH, INGREDIENTS_JSON)
        Ingredient.objects.all().delete()

        with open(path, 'r') as f:
            Ingredient.objects.bulk_create(
                objs=[Ingredient(**x) for x in json.load(f)]
            )
