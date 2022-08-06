from django.core.management.base import BaseCommand
import csv
from web.models import Students
from core.settings import BASE_DIR

class Command(BaseCommand):
    help = 'importing all the cs50 registered users into app User model'

    def __init__(self, *args, **kwargs):
        super(Command,self).__init__(*args, **kwargs)
        self.path = (BASE_DIR / 'account_user.csv')
        #self.path = (BASE_DIR / 'test.csv')

    def handle(self, *args, **options):
        with open(self.path) as f:
            reader = csv.reader(f)
            for row in reader:
                print(row[0])
                user = Students.objects.get_or_create(
                    phone = row[0],
                    name = f"{row[1]} - {row[2]}",
                    email = row[3],
                    )
                print(user)