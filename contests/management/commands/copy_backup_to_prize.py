from django.core.management.base import BaseCommand
from contests.models import Contest

class Command(BaseCommand):
    help = 'Copy data from 상금_backup to 상금'

    def handle(self, *args, **kwargs):
        contests = Contest.objects.all()
        for contest in contests:
            if contest.상금_backup is not None:
                contest.상금 = contest.상금_backup
                contest.save()
        self.stdout.write(self.style.SUCCESS('Successfully copied 상금_backup to 상금'))
