# -*- coding: utf-8 -*-
"""
:mod:`module-name-here` -- Description here 
===================================

.. module:: module-name-here
   :platform: Unix, Windows
   :synopsis: complete.
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import logging
import os
import unittest

import log_config

from api import create_app

logger = logging.getLogger(__name__)


class TestCreateTermEndpoint(unittest.TestCase):
    def setUp(self):
        try:
            assert os.getenv('CONFIGURATION', None)
            self.app = create_app().test_client()
        except Exception:
            logger.debug("did you forgot to add the CONFIGURATION"
                         " environmental variable?")
            raise

    def test_create_fails_because_missing_headers(self):
        response = self.app.get('/')
        self.assertEquals(response.status_code, 404)

