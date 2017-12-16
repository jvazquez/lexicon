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

    def test_create_fails_because_missing_headers(self):
        response = self.app.post('/', content_type='application/html')
        obtained_code = response.status_code
        self.assertEquals(obtained_code, api.constants.ERROR)
        self.assertEquals(response.content_type, 'application/json')

    def test_create_validates_wrong_payload(self):
        self.skipTest("Not yet")
        response = self.app.post('/', data=json.dumps({'term': None}),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEquals(obtained_code, api.constants.ERROR)
        logger.debug(response.data)
