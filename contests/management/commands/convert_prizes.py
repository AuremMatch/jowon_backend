from django.core.management.base import BaseCommand
from contests.models import Contest

class Command(BaseCommand):
    help = 'Convert 상금 field from CharField to DecimalField'

    def handle(self, *args, **kwargs):
        contests = Contest.objects.all()
        for contest in contests:
            if contest.상금:
                converted_value = convert_string_to_float(contest.상금)
                if converted_value is not None:
                    contest.상금_backup = converted_value
                    contest.save()
        self.stdout.write(self.style.SUCCESS('Successfully converted 상금 field'))

def convert_string_to_float(s):
    try:
        return float(s.replace(',', '').replace('₩', '').strip())
    except ValueError:
        return None

