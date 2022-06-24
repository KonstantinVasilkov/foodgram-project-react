import csv

from django.core.management import BaseCommand

from recipes.models import Ingredient
from recipes.models import Tag


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        model = kwargs['model']
        with open(path, 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            if model == 'Ingredient':
                for row in reader:
                    Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1]
                    )
            if model == 'Tag':
                for row in reader:
                    Tag.objects.get_or_create(
                        name=row[0],
                        color=row[1],
                        slug=row[2]
                    )
