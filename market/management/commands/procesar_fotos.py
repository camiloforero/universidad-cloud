from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from market import batch_jobs

class Command(BaseCommand):
    help = "Reloads all local and national offices' stats in measures such as opens, applied, accepted, realized and completed experiencies"

    def handle(self, *args, **options):
        batch_jobs.batch_converter()
