from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import requests
import time
from ...services import data_processor
import os
import json


class Command(BaseCommand):
    help = 'Polling service for fetching data'

    def add_arguments(self, parser):
        parser.add_argument('read_from_file', nargs='+', type=bool)

    def handle(self, *args, **options):
        while True:
            print 'Started reading data......'
            if not options['read_from_file'][0]:
                r = requests.get(url=settings.POLLING_ENDPOINT)
                data = r.json()
            else:

                file_ = open(os.path.join(settings.BASE_DIR, 'data.txt'))
                data = json.loads(file_.read())
            processor = data_processor.Processor(data)
            processor.process_updates()
            time.sleep(settings.POLLING_INTERVAL)
