from django.core.management.base import BaseCommand
import csv
from web.models import TA
from core.settings import BASE_DIR

class Command(BaseCommand):
    help = 'importing all the cs50 TAs from csv file'

    def __init__(self, *args, **kwargs):
        super(Command,self).__init__(*args, **kwargs)
        self.path = (BASE_DIR / 'cs50_TAs.csv')

    def handle(self, *args, **options):
        with open(self.path) as f:
            reader = csv.reader(f)
            for row in reader:
                print(row[0])
                user = TA.objects.get_or_create(discord_id=row[0])
                print(user)