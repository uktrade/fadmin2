from django.core.management.base import BaseCommand, CommandError
from csvimport.costcentre import importcostcentres
import csv


class Command(BaseCommand):
    help = 'Import CC hierarchy from csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_path')
        parser.add_argument('type')

# pass the file path as an argument
# second argument will define the content of the file

    def handle(self, *args, **options):
        path = options.get('csv_path')
        importcostcentres(path)







