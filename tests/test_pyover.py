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

    def test_no_token(self):
        """
        Test if passing no token gives a RuntimeError.
        """
        self.assertRaises(RuntimeError, PyOver, '', 'asdas')

    def test_no_user_key(self):
        """
        Test if passing no token gives a RuntimeError.
        """
        self.assertRaises(RuntimeError, PyOver, 'asdas', '')

    def test_wrong_credentials(self):
        """
        Test what happens when trying to send a message with the wrong creds.
        """
        test_instance = PyOver('foo', 'foo')
        self.assertRaises(requests.HTTPError,
                          test_instance.send_message,
                          'Test message!')

    @unittest.skipUnless(
        (os.environ.get('PUSHOVER_API_TOKEN')
         and os.environ.get('PUSHOVER_USER_KEY')),
        'The environment variables `PUSHOVER_USER_KEY` and `PUSHOVER_API_TOKEN` are not set.')
    def test_message(self):
        """
        Test sending a correct message.
        """
        test_instance = PyOver(self.token, self.user_key)
        output = test_instance.send_message("Test message")
        self.assertEqual(output['status'], 1)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
