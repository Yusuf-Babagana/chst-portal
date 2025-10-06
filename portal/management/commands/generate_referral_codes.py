from django.core.management.base import BaseCommand
from portal.models import ReferralCode
import random
import string


class Command(BaseCommand):
    help = 'Generate unique referral codes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of referral codes to generate (default: 100)'
        )

    def handle(self, *args, **options):
        count = options['count']
        generated = 0

        self.stdout.write(f'Generating {count} referral codes...')

        for i in range(count):
            code = self.generate_unique_code()
            if code:
                ReferralCode.objects.create(code=code)
                generated += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated {generated} referral codes!')
        )

    def generate_unique_code(self):
        for _ in range(10):
            code = 'CHSTH-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not ReferralCode.objects.filter(code=code).exists():
                return code
        return None
