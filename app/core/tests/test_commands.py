""" Test costume Django Management Command """

# mocking a piece code using patch method
from unittest.mock import patch

# import OperationalError from psycopg2 for handle DataBase Error
from psycopg2 import OperationalError as Psycopg2Error

# import call_cammand for using our management command('wait_for_db')
from django.core.management import call_command
# other django built_in
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class TestCommands(SimpleTestCase):
    """ Test DB when available """
    def test_wait_for_db_ready(self, patched_check):
        # test waiting database when database is ready
        patched_check.return_value = True

        # call wait_for_db Command
        call_command('wait_for_db')

        # check once returned db with our arguments or not
        patched_check.assert_called_once_with(databases=['default'])

    """ Test DB when unavailable """
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        # test waiting for DB when getting OperationalError
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
