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
from terms.models import Terms, RelatedTerms
from tests.fixtures.models import TermsFactory

logger = logging.getLogger(__name__)


class TermsBaseTestCase(unittest.TestCase):
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


class TestCreateTermEndpoint(TermsBaseTestCase):
    def test_create_fails_because_it_does_not_receive_data(self):
        response = self.app.post('/term/', content_type='application/html')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.ERROR)
        self.assertEqual(response.content_type, 'application/json')

    def test_create_validates_none_word_value(self):
        stub = {'word': None, 'definition': 'Something'}
        response = self.app.post('/term/', data=json.dumps(stub),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.ERROR)

    def test_create_validates_word_as_space(self):
        stub = {'word': ' ', 'definition': 'Something important'}
        response = self.app.post('/term/', data=json.dumps(stub),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.ERROR)

    def test_create_validates_word_because_is_emtpy(self):
        stub = {'word': '', 'definition': 'Something important'}
        response = self.app.post('/term/', data=json.dumps(stub),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.ERROR)

    def test_create_validates_empty_description(self):
        response = self.app.post('/term/', data=json.dumps({'word': 'threading',
                                                       'definition': ''}),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.ERROR)

    def test_create_validates_space_description(self):
        response = self.app.post('/term/', data=json.dumps({'word': 'threading',
                                                       'definition': ' '}),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.ERROR)

    def test_create_word_will_persist_information(self):
        stub = {'word': 'threading', 'definition': 'Thread of life'}
        response = self.app.post('/term/', data=json.dumps(stub),
                                 content_type='application/json')
        obtained_code = response.status_code
        self.assertEqual(obtained_code, constants.CREATED_STATUS_CODE)


class TestCreateRelatedTermsEndpoint(TermsBaseTestCase):
    def test_create_relation_fails_because_user_sends_empty_post(self):
        response = self.app.post('/related-terms/',
                                 content_type='application/json')
        self.assertEqual(response.status_code, constants.ERROR)

    def test_create_relation_fails_because_term_does_not_exist(self):
        terms = TermsFactory()
        sample = {'term_id': terms.id, 'related_term_id': terms.id + 1}
        response = self.app.post('/related-terms/', data=json.dumps(sample),
                                 content_type='application/json')
        self.assertEqual(response.status_code, constants.NOT_FOUND)
        output = json.loads(response.data)
        self.assertEqual(output.get('message'), constants.TERM_NOT_FOUND)

    def test_create_relation_fails_because_related_term_does_not_exist(self):
        term = TermsFactory()
        sample = {'term_id': term.id + 1, 'related_term_id': term.id}
        response = self.app.post('/related-terms/', data=json.dumps(sample),
                                 content_type='application/json')
        self.assertEqual(response.status_code, constants.NOT_FOUND)
        output = json.loads(response.data)
        self.assertEqual(output.get('message'), constants.TERM_NOT_FOUND)

    def test_create_related_term_will_return_created_related_term_status(self):
        term = TermsFactory()
        related_term = TermsFactory()
        sample = {'term_id': term.id,
                  'related_term_id': related_term.id}
        response = self.app.post('/related-terms/', data=json.dumps(sample),
                                 content_type='application/json')
        self.assertEqual(response.status_code,
                         constants.CREATED_RELATED_TERM)
        output = json.loads(response.data)
        related_term_id = output.get('related_term').get('related_term_id')
        term_id = output.get('related_term').get('term_id')
        self.assertEqual(related_term_id, related_term.id)
        self.assertEqual(term_id, term.id)
        self.assertEqual(output.get('message'), constants.CREATED_RELATED_TERM)


class TestDeleteTermEndpoint(TermsBaseTestCase):
    def test_will_return_404_when_trying_to_delete_unexistent_term(self):
        response = self.app.delete('/terms/{}'.format(100),
                                   content_type='application/json')
        self.assertEqual(response.status_code, constants.NOT_FOUND)
        output = json.loads(response.data)
        self.assertEquals(output.get('message'), constants.TERM_NOT_FOUND)

    def test_will_return_404_when_trying_to_delete_without_id(self):
        response = self.app.delete('/terms',
                                   content_type='application/json')
        self.assertEqual(response.status_code, constants.NOT_FOUND)

    def test_will_return_deleted_when_trying_to_delete(self):
        tf = TermsFactory()
        response = self.app.delete('/terms/{}'.format(tf.id),
                                   content_type='application/json')
        self.assertEqual(response.status_code, constants.DELETED)
        output = json.loads(response.data)
        self.assertEquals(output.get('message'), constants.TERM_DELETED)

    def test_will_be_logically_deleted(self):
        tf = TermsFactory()
        response = self.app.delete('/terms/{}'.format(tf.id),
                                   content_type='application/json')
        self.assertEqual(response.status_code, constants.DELETED)
        output = json.loads(response.data)
        self.assertEquals(output.get('message'), constants.TERM_DELETED)
        witness = Terms.query.get(tf.id)
        self.assertTrue(witness.deleted)


class TestUpdateTermEndpoint(TermsBaseTestCase):
    def test_will_return_404_when_trying_to_update_unexistent_term(self):
        response = self.app.patch('/terms/{}'.format(100),
                                  content_type='application/json')
        self.assertEqual(response.status_code, constants.NOT_FOUND)
        output = json.loads(response.data)
        self.assertEquals(output.get('message'), constants.TERM_NOT_FOUND)

    def test_will_return_error_when_payload_is_missing(self):
        term = TermsFactory()
        response = self.app.patch('/terms/{}'.format(term.id),
                                  content_type='application/json')
        self.assertEqual(response.status_code, constants.ERROR)
        output = json.loads(response.data)
        self.assertEquals(output.get('message'), constants.MISSING_PAYLOAD)

    def test_will_update_when_payload_is_ok(self):
        term = TermsFactory()
        stub = {'word': 'A word', 'definition': 'Is what we need',
                'extra': 'This will not affect'}
        response = self.app.patch('/terms/{}'.format(term.id),
                                  data=json.dumps(stub),
                                  content_type='application/json')
        self.assertEqual(response.status_code, constants.UPDATED)
        output = json.loads(response.data)
        self.assertEquals(output.get('message'), constants.TERM_UPDATED)

    def test_will_fail_when_name_is_not_none(self):
        term = TermsFactory()
        stub = {'word': None, 'definition': 'Is what we need',
                'extra': 'This will not affect'}
        response = self.app.patch('/terms/{}'.format(term.id),
                                  data=json.dumps(stub),
                                  content_type='application/json')
        self.assertEqual(response.status_code, constants.ERROR)
        output = json.loads(response.data)
        expected = {'word': ['Field may not be null.']}
        self.assertEquals(output.get('message'), expected)

    def test_will_fail_when_name_is_not_space(self):
        term = TermsFactory()
        stub = {'word': ' ', 'definition': 'Is what we need',
                'extra': 'This will not affect'}
        response = self.app.patch('/terms/{}'.format(term.id),
                                  data=json.dumps(stub),
                                  content_type='application/json')
        self.assertEqual(response.status_code, constants.ERROR)
        output = json.loads(response.data)
        expected = {'word': ['Word cannot be a space']}
        self.assertEquals(output.get('message'), expected)

    def test_will_fail_when_definition_is_none(self):
        term = TermsFactory()
        stub = {'word': 'Something', 'definition': None,
                'extra': 'This will not affect'}
        response = self.app.patch('/terms/{}'.format(term.id),
                                  data=json.dumps(stub),
                                  content_type='application/json')
        self.assertEqual(response.status_code, constants.ERROR)
        output = json.loads(response.data)
        expected = {'definition': ['Field may not be null.']}
        self.assertEquals(output.get('message'), expected)

    def test_will_fail_when_definition_is_space(self):
        term = TermsFactory()
        stub = {'word': 'Something', 'definition': ' ',
                'extra': 'This will not affect'}
        response = self.app.patch('/terms/{}'.format(term.id),
                                  data=json.dumps(stub),
                                  content_type='application/json')
        self.assertEqual(response.status_code, constants.ERROR)
        output = json.loads(response.data)
        expected = {'definition': ['Word cannot be a space']}
        self.assertEquals(output.get('message'), expected)


class TestGetTermEndpoint(TermsBaseTestCase):
    def test_will_return_404_when_trying_to_get_unexistent_term(self):
        response = self.app.get('/terms/{}'.format(100),
                                content_type='application/json')
        self.assertEqual(response.status_code, constants.NOT_FOUND)
        output = json.loads(response.data)
        self.assertEquals(output.get('message'), constants.TERM_NOT_FOUND)

    def test_will_return_term_when_it_exists(self):
        term = TermsFactory()
        response = self.app.get('/terms/{}'.format(term.id),
                                content_type='application/json')
        self.assertEqual(response.status_code, constants.FOUND)
        # output = json.loads(response.data)
        # self.assertEquals(output.get('message'), constants.TERM_NOT_FOUND)

