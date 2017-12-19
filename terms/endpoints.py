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

import marshmallow
from flask import Blueprint, jsonify, make_response, request

from app import db
from constants import (CREATED_STATUS_CODE, ERROR, MISSING_PAYLOAD,
                       NOT_FOUND, TERM_NOT_FOUND)
from terms.models import Terms, TermsSchema
from terms.models import RelatedTerms
from terms.models import RelatedTermsSchema

terms_bp = Blueprint('terms', __name__)
_ = gettext.gettext
logger = logging.getLogger(__name__)


@terms_bp.route('/term/', methods=['POST'])
def create_term():
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({'message': MISSING_PAYLOAD}),
                             ERROR)
    data, errors = TermsSchema().load(request.json)
    if errors:
        return make_response(jsonify(errors), ERROR)

    term = Terms(**json_data)
    db.session.add(term)
    db.session.commit()
    term_schema = TermsSchema()
    data = term_schema.dump(Terms.query.get(term.id))
    return make_response(jsonify(data), CREATED_STATUS_CODE)


@terms_bp.route('/related-terms/', methods=['POST'])
def create_relation():
    json_data = request.get_json()
    if json_data is None:
        make_response(jsonify({'message': MISSING_PAYLOAD}), ERROR)

    if not json_data.get('term_id') or not json_data.get('related_term_id'):
        return make_response(jsonify({'message': MISSING_PAYLOAD}),
                             ERROR)

    term = Terms.query.get(json_data.get('term_id'))
    if not term:
        return make_response(jsonify({'message': TERM_NOT_FOUND}),
                             NOT_FOUND)
    related_term = Terms.query.get(json_data['related_term_id'])
    if not related_term:
        return make_response(jsonify({'message': TERM_NOT_FOUND}),
                             NOT_FOUND)
    rt = RelatedTerms(**json_data)
    db.session.add(rt)
    db.session.commit()
    related_terms_schema = RelatedTermsSchema()
    data = related_terms_schema.dump(RelatedTerms.query.get(rt.id))
    return make_response(jsonify(data), CREATED_STATUS_CODE)
