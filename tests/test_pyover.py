#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyover
----------------------------------

Tests for `pyover` module.
"""

import unittest
import os
import requests

from pyover import PyOver


class TestPyover(unittest.TestCase):

    def setUp(self):
        self.token = os.environ.get('PUSHOVER_API_TOKEN', False)
        self.user_key = os.environ.get('PUSHOVER_USER_KEY', False)
        if self.token and self.user_key:
            self.test_instance = PyOver(self.token, self.user_key)

    def test_no_token(self):
        """
        Test if passing no token gives a RuntimeError.
        """
        self.assertRaises(RuntimeError, PyOver, '', 'deadbeaf')

    def test_no_user_key(self):
        """
        Test if passing no token gives a RuntimeError.
        """
        self.assertRaises(RuntimeError, PyOver, 'deadbeaf', '')

    def test_wrong_credentials(self):
        """
        Test what happens when trying to send a message with the wrong creds.
        """
        failed_instance = PyOver('deadbeaf', 'deadbeaf')
        self.assertRaises(requests.HTTPError,
                          failed_instance.send_message,
                          'Test message!')

    @unittest.skipUnless(
        (os.environ.get('PUSHOVER_API_TOKEN')
         and os.environ.get('PUSHOVER_USER_KEY')),
        'Variables `PUSHOVER_USER_KEY` and `PUSHOVER_API_TOKEN` are not set.')
    def test_message(self):
        """
        Test sending a correct message.
        """
        output = self.test_instance.send_message('Test message')
        self.assertEqual(output['status'], 1)

    @unittest.skipUnless(
        (os.environ.get('PUSHOVER_API_TOKEN')
         and os.environ.get('PUSHOVER_USER_KEY')
         and os.environ.get('PUSHOVER_DEVICE')),
        '`PUSHOVER_USER_KEY`, `PUSHOVER_API_TOKEN` `PUSHOVER_DEVICE` are not set.')
    def test_message_with_device(self):
        """
        Test sending a correct message.
        """
        self.test_instance = PyOver(self.token,
                                    self.user_key,
                                    os.environ['PUSHOVER_DEVICE'])
        output = self.test_instance.send_message('Test message with device.')
        self.assertEqual(output['status'], 1)

    @unittest.skipUnless(
        (os.environ.get('PUSHOVER_API_TOKEN')
         and os.environ.get('PUSHOVER_USER_KEY')),
        'Variables `PUSHOVER_USER_KEY` and `PUSHOVER_API_TOKEN` are not set.')
    def test_message_with_title(self):
        """
        Tests sending a message with a custom title.
        """
        output = self.test_instance.send_message('Test message with title.',
                                                 title='Some custom title.')
        self.assertEqual(output['status'], 1)

    @unittest.skipUnless(
        (os.environ.get('PUSHOVER_API_TOKEN')
         and os.environ.get('PUSHOVER_USER_KEY')),
        'Variables `PUSHOVER_USER_KEY` and `PUSHOVER_API_TOKEN` are not set.')
    def test_message_with_url(self):
        """
        Tests sending a message with a URL attached.
        """
        output = self.test_instance.send_message(
            'Test message with URL.',
            url='https://github.com/ainmosni/pyover'
        )
        self.assertEqual(output['status'], 1)

    @unittest.skipUnless(
        (os.environ.get('PUSHOVER_API_TOKEN')
         and os.environ.get('PUSHOVER_USER_KEY')),
        'Variables `PUSHOVER_USER_KEY` and `PUSHOVER_API_TOKEN` are not set.')
    def test_message_with_url_title(self):
        """
        Tests sending a message with a URL and title attached.
        """
        output = self.test_instance.send_message(
            'Test message with URL and URL title.',
            url='https://github.com/ainmosni/pyover',
            url_title='PyOver github page.'
        )
        self.assertEqual(output['status'], 1)

    @unittest.skipUnless(
        (os.environ.get('PUSHOVER_API_TOKEN')
         and os.environ.get('PUSHOVER_USER_KEY')),
        'Variables `PUSHOVER_USER_KEY` and `PUSHOVER_API_TOKEN` are not set.')
    def test_message_with_timestamp(self):
        """
        Tests sending a message with a custom timestamp.
        """
        import datetime
        import calendar
        timestamp = datetime.datetime(1981, 10, 26, 4, 35)
        output = self.test_instance.send_message(
            'Test message with timestamp.',
            timestamp=calendar.timegm(timestamp.utctimetuple())
        )
        self.assertEqual(output['status'], 1)

    @unittest.skipUnless(
        (os.environ.get('PUSHOVER_API_TOKEN')
         and os.environ.get('PUSHOVER_USER_KEY')),
        'Variables `PUSHOVER_USER_KEY` and `PUSHOVER_API_TOKEN` are not set.')
    def test_message_with_priorities(self):
        """
        Test sending a message with all priorities set.
        """
        for priority in range(-1, 3):
            output = self.test_instance.send_message('Test message with pri {}'
                                                     .format(priority),
                                                     prority=priority)
            self.assertEqual(output['status'], 1)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
