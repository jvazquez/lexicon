# -*- coding: utf-8 -*-
"""
:mod:`validators` -- Validators are used to valid the user input
===================================

.. module:: validators
   :platform: Unix, Windows
   :synopsis: complete.
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import logging
import gettext

from collections import deque

from api.terms.models import Terms

_ = gettext.gettext
logger = logging.getLogger(__name__)


class ValidateCreate:
    def __init__(self, *args, **kwargs):
        self.errors = []
        self.excluded_from_validation = []

        if 'exclude_fields' in kwargs.keys():
            self.map_exclude_fields(kwargs['exclude_fields'])

    def map_exclude_fields(self, data):
        pass

    def get_errors(self):
        return self.errors

    def validate(self, data):
        try:
            assert len(data) > 0
        except AssertionError:
            logger.exception('Payload is empty')
            self.errors.append({'msg': _('Received empty information')})
            return False

        attributes = deque(filter(lambda term: term.startswith('_') is False,
                                  Terms.__dict__.keys()))
        try:
            assert data.keys() == attributes.keys()
        except AssertionError:
            logger.exception('Missing data keys')
            self.errors.append({'msg': _('You are missing crucial data.')})
            return False

        return True

