from django.core.management.base import BaseCommand
import openpyxl
from web.models import ClassAttend
from core.settings import BASE_DIR
from datetime import datetime
import os

class Command(BaseCommand):
    help = 'importing all the cs50 registered users into app User model'

    def __init__(self, *args, **kwargs):
        super(Command,self).__init__(*args, **kwargs)
        date = str(datetime.today().date())
        path = BASE_DIR / f'../{date}'

        if not os.path.exists(path):
            os.makedirs(path)

        self.path = (BASE_DIR / f'../{date}/ClassAttend.xlsx')
        #self.path = (BASE_DIR / 'test.csv')

    def handle(self, *args, **options):
        objects = ClassAttend.objects.all().values_list('name', 'email', 'phone', 'ticket', 'canceled', 'entered', 'created_time', 'updated_time')
        wb = openpyxl.Workbook()
        sheet = wb.active

        for i in objects:
            sheet.append(list(map(str, i)))
        
        wb.save(self.path)
        