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
import constants

from app import app
from orm import db
from terms.models import Terms, RelatedTerms
from tests.fixtures.models import TermsFactory

logger = logging.getLogger(__name__)


class TestCreateTermEndpoint(unittest.TestCase):
    def setUp(self):
        try:
            assert os.getenv('CONFIGURATION', None)
            self.lexicon = app
            self.app = self.lexicon.test_client()
            self.lexicon.app_context().push()
        except Exception:
            logger.debug("did you forgot to add the CONFIGURATION"
                         " environmental variable?")
            raise

    def tearDown(self):
        with self.lexicon.app_context() as ctx:
            ctx.push()
            Terms.query.delete()

    def test_create_fails_because_it_does_not_receive_data(self):
        response = self.app.post('/', content_type='application/html')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.ERROR)
        self.assertEqual(response.content_type, 'application/json')

    def test_create_validates_none_word_value(self):
        stub = {'word': None, 'definition': 'Something'}
        response = self.app.post('/', data=json.dumps(stub),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.ERROR)

    def test_create_validates_word_as_space(self):
        stub = {'word': ' ', 'definition': 'Something important'}
        response = self.app.post('/', data=json.dumps(stub),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.ERROR)

    def test_create_validates_word_because_is_emtpy(self):
        stub = {'word': '', 'definition': 'Something important'}
        response = self.app.post('/', data=json.dumps(stub),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.ERROR)

    def test_create_validates_empty_description(self):
        response = self.app.post('/', data=json.dumps({'word': 'threading',
                                                       'definition': ''}),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.ERROR)

    def test_create_validates_space_description(self):
        response = self.app.post('/', data=json.dumps({'word': 'threading',
                                                       'definition': ' '}),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.ERROR)

    def test_create_word_will_persist_information(self):
        stub = {'word': 'threading', 'definition': 'Thread of life'}
        response = self.app.post('/', data=json.dumps(stub),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.CREATED_STATUS_CODE)


class TestCreateRelatedTermsEndpoint(unittest.TestCase):
    def setUp(self):
        try:
            assert os.getenv('CONFIGURATION', None)
            self.lexicon = app
            self.app = self.lexicon.test_client()
            self.lexicon.app_context().push()
            RelatedTerms.query.delete()
            Terms.query.delete()
        except Exception:
            logger.debug("did you forgot to add the CONFIGURATION"
                         " environmental variable?")
            raise

    def tearDown(self):
        with self.lexicon.app_context() as ctx:
            RelatedTerms.query.delete()
            Terms.query.delete()

    def test_create_relation_fails_because_user_sends_empty_post(self):
        response = self.app.post('/relation/',
                                 content_type='application/json')
        self.assertEqual(response.status_code, constants.ERROR)

    def test_create_relation_fails_because_term_does_not_exist(self):
        terms = TermsFactory()
        sample = {'term_id': terms.id, 'related_term_id': terms.id + 1}
        response = self.app.post('/relation/', data=json.dumps(sample),
                                 content_type='application/json')
        self.assertEqual(response.status_code, constants.NOT_FOUND)
        output = json.loads(response.data)
        self.assertEqual(output.get('message'), constants.TERM_NOT_FOUND)

    def test_create_relation_fails_because_related_term_does_not_exist(self):
        term = TermsFactory()
        sample = {'term_id': term.id + 1, 'related_term_id': term.id}
        response = self.app.post('/relation/', data=json.dumps(sample),
                                 content_type='application/json')
        self.assertEqual(response.status_code, constants.NOT_FOUND)
        output = json.loads(response.data)
        self.assertEqual(output.get('message'), constants.TERM_NOT_FOUND)

    def test_create_term_will_return(self):
        term = TermsFactory()
        related_term = TermsFactory()
        sample = {'term_id': term.id,
                  'related_term_id': related_term.id}
        response = self.app.post('/relation/', data=json.dumps(sample),
                                 content_type='application/json')
        self.assertEqual(response.status_code,
                         constants.CREATED_STATUS_CODE)
        output = json.loads(response.data)
        related_term_id = output[0].get('related_term_id')
        term_id = output[0].get('term_id')
        self.assertEqual(related_term_id, related_term.id)
        self.assertEqual(term_id, term.id)
