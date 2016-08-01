import datetime
from django.core.management.base import BaseCommand, CommandError
from registration.models import Registration
from registration.iamporter import Iamporter, get_access_token
from constance import config

class Command(BaseCommand):
    help = 'Check person who paid but not registrated'

    def handle(self, *args, **options):
        paid_registrations = Registration.objects.filter(payment_status='paid').values_list('email', flat=True)
        paid_registrations = set(paid_registrations)
        access_token = get_access_token(config.IMP_API_KEY, config.IMP_API_SECRET)
        imp_client = Iamporter(access_token)
        # Use hard coded date only for pycon 2016.
        paid_pg = imp_client.get_paid_list(since=datetime.datetime(2016, 1, 1))
        paid_pg = map(lambda x: x['buyer_email'], paid_pg)
        paid_pg = set(paid_pg)
        paid_only_set = paid_pg - paid_registrations
        for person in paid_only_set:
            print(person)
