# -*- coding: utf-8 -*-
"""
:mod:`test_validators` -- Test for the validator test file
===================================

.. module:: test_validators
   :platform: Unix, Windows
   :synopsis: Handles the testing of the validators
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import logging
import unittest

import log_config

from api.terms import validators


class TestValidateCreate(unittest.TestCase):
    def test_validate_rejects_empty_dict(self):
        data = {}
        validator = validators.ValidateCreate()
        self.assertFalse(validator.validate(data))

    def test_validate_will_have_descriptive_message(self):
        validator = validators.ValidateCreate()
        self.assertFalse(validator.validate({}))
        self.assertTrue(len(validator.get_errors()) > 0)

    def test_validate_with_partial_keys_will_be_true(self):
        validator = validators.ValidateCreate({'exclude': ['created', 'updated']})


