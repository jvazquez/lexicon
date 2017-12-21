# -*- coding: utf-8 -*-
"""
:mod:`endpoints` -- Endpoints for the terms application
===================================

.. module:: endpoints
   :platform: Unix, Windows
   :synopsis: Handles the several endpoints of terms
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import gettext
import logging

import werkzeug

from flask import Blueprint, jsonify, make_response, request

import constants

from app import db
from terms.models import Terms, TermsSchema
from terms.models import RelatedTerms
from terms.models import RelatedTermsSchema
import marshmallow

terms_bp = Blueprint('terms', __name__)
_ = gettext.gettext
logger = logging.getLogger(__name__)


@terms_bp.route('/term/', methods=['POST'])
def create_term():
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({'message': constants.MISSING_PAYLOAD}),
                             constants.ERROR)
    data, errors = TermsSchema().load(request.json)
    if errors:
        return make_response(jsonify(errors), constants.ERROR)

    term = Terms(**json_data)
    db.session.add(term)
    db.session.commit()
    term_schema = TermsSchema()
    data = term_schema.dump(Terms.query.get(term.id))
    return make_response(jsonify(data), constants.CREATED_STATUS_CODE)


@terms_bp.route('/related-terms/', methods=['POST'])
def create_relation():
    try:
        json_data = request.get_json()

        if not json_data.get('term_id') or not json_data.get('related_term_id'):
            return make_response(jsonify({'message': constants.MISSING_PAYLOAD}),
                                constants.ERROR)

        term = Terms.query.get(json_data.get('term_id'))
        if not term:
            return make_response(jsonify({'message': constants.TERM_NOT_FOUND}),
                                constants.NOT_FOUND)
        related_term = Terms.query.get(json_data['related_term_id'])
        if not related_term:
            return make_response(jsonify({'message': constants.TERM_NOT_FOUND}),
                                constants.NOT_FOUND)

        rt = RelatedTerms(**json_data)
        db.session.add(rt)
        db.session.commit()
        related_terms_schema = RelatedTermsSchema()
        created_related_term = related_terms_schema.dump(
            RelatedTerms.query.get(rt.id)
        )
        return make_response(
            jsonify(
                {
                    'message': constants.CREATED_RELATED_TERM,
                    'related_term': created_related_term.data
                }
            ),
            constants.CREATED_STATUS_CODE
        )
    except werkzeug.exceptions.BadRequest:
        return make_response(jsonify({'message': constants.MISSING_PAYLOAD}),
                             constants.ERROR)


@terms_bp.route('/terms/<int:_id>', methods=['DELETE'])
def delete_term(_id):
    term = Terms.query.get(_id)
    if not term:
        return make_response(jsonify({'message': constants.TERM_NOT_FOUND}),
                             constants.NOT_FOUND)
    term.deleted = True
    db.session.add(term)
    db.session.commit()
    return make_response(jsonify({'message': constants.TERM_DELETED}),
                         constants.DELETED)


@terms_bp.route('/terms/<int:_id>', methods=['PATCH'])
def update_term(_id):
    term = Terms.query.get(_id)
    if not term:
        return make_response(jsonify({'message': constants.TERM_NOT_FOUND}),
                             constants.NOT_FOUND)
    try:
        json_data = request.get_json()
        terms_schema = TermsSchema(strict=True)
        terms_schema_data = terms_schema.load(json_data)
        term.word = terms_schema_data.data.get('word')
        term.definition = terms_schema_data.data.get('definition')
        db.session.add(term)
        db.session.commit()
        updated_record = terms_schema.dump(Terms.query.get(term.id))
        return make_response(
            jsonify(
                {
                    "message": constants.TERM_UPDATED,
                    "term": updated_record.data
                }
            ),
            constants.UPDATED
        )

    except werkzeug.exceptions.BadRequest:
        return make_response(jsonify({'message': constants.MISSING_PAYLOAD}),
                             constants.ERROR)
    except marshmallow.exceptions.ValidationError as error:
        response = make_response(
            jsonify(
                    {
                        'message': error.messages
                    }
            ),
            constants.ERROR
        )
        return response


@terms_bp.route('/terms/<int:_id>', methods=['GET'])
def get_term(_id):
    term = Terms.query.get(_id)
    if not term:
        return make_response(jsonify({'message': constants.TERM_NOT_FOUND}),
                             constants.NOT_FOUND)

