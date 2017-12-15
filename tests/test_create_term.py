# -*- coding: utf-8 -*-
"""
:mod:`module-name-here` -- Description here 
===================================

.. module:: module-name-here
   :platform: Unix, Windows
   :synopsis: complete.
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import os
import unittest

from api import create_app


class TestCreateTermEndpoint(unittest.TestCase):
    def test_create_fails_because_missing_headers(self):
        self.assertEquals(os.getenv('CONFIGURATION'), 'testing')

