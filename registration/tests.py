# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from constance.test import override_config
from django_dynamic_fixture import G

from models import Option, Registration

User = get_user_model()


@override_config(REGISTRATION_OPEN=datetime.date.today(), REGISTRATION_CLOSE=datetime.date.today()+datetime.timedelta(days=1))
class RegistrationTest(TestCase):
    def test_patron_has_additional_price(self):
        option = Option.objects.create(name='patron', price=1000, has_additional_price=True, is_active=True)
        user = User.objects.create_user('testname', 'test@test.com', 'testpassword')
        self.client.login(username='testname', password='testpassword')
        response = self.client.get(reverse('registration_payment', args=[option.id]))
        self.assertIn('additional_price', response.context['form'].fields)

    def test_transaction_id_is_not_required(self):
        registration = G(Registration, transaction_code='')
        self.assertNotEqual(registration.id, None)
