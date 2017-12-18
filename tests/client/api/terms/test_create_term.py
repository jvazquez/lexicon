# -*- coding: utf-8 -*-
"""
:mod:`module-name-here` -- Description here 
===================================

.. module:: module-name-here
   :platform: Unix, Windows
   :synopsis: complete.
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import json
import logging
import os
import unittest

import log_config
import api.constants

from api.terms.models import Terms


logger = logging.getLogger(__name__)


class TestCreateTermEndpoint(unittest.TestCase):
    def setUp(self):
        try:
            assert os.getenv('CONFIGURATION', None)
            self.app = api.create_app().test_client()
        except Exception:
            logger.debug("did you forgot to add the CONFIGURATION"
                         " environmental variable?")
            raise

    def tearDown(self):
        Terms.query.delete()

    def test_create_fails_because_missing_headers(self):
        response = self.app.post('/', content_type='application/html')
        obtained_code = response.status_code
        self.assertEquals(obtained_code, api.constants.ERROR)
        self.assertEquals(response.content_type, 'application/json')

    def test_create_validates_none_word_value(self):
        response = self.app.post('/', data=json.dumps({'word': None,
                                                       'definition': 'Something'}),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEquals(obtained_code, api.constants.ERROR)

    def test_create_validates_word_as_space(self):
        response = self.app.post('/', data=json.dumps({'word': ' ', 'definition':
                                                       'Something important'}),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEquals(obtained_code, api.constants.ERROR)

    def test_create_validates_word_because_is_emtpy(self):
        response = self.app.post('/', data=json.dumps({'word': '', 'definition':
                                                       'Something important'}),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEquals(obtained_code, api.constants.ERROR)

    def test_create_validates_empty_description(self):
        response = self.app.post('/', data=json.dumps({'word': 'threading',
                                                       'definition': ''}),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEquals(obtained_code, api.constants.ERROR)

    def test_create_validates_space_description(self):
        response = self.app.post('/', data=json.dumps({'word': 'threading',
                                                       'definition': ' '}),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEquals(obtained_code, api.constants.ERROR)

    def test_create_word_will_persist_information(self):
        response = self.app.post('/', data=json.dumps({'word': 'threading',
                                                       'definition': 'Thread of'
                                                       ' life'}),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEquals(obtained_code, api.constants.CREATED_STATUS_CODE)

