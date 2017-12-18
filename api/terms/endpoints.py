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
import json
import logging

import marshmallow
from flask import Blueprint, jsonify, make_response, request

from api import db
from api.constants import CREATED_STATUS_CODE, ERROR, MISSING_PAYLOAD
from api.terms.models import Terms, TermsSchema

terms_bp = Blueprint('terms', __name__)
_ = gettext.gettext
logger = logging.getLogger(__name__)


@terms_bp.route('/', methods=['POST'])
def create_term():
    try:
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': MISSING_PAYLOAD}),
                                 ERROR)
        data, errors = TermsSchema(strict=True).load(request.json)
        if errors:
            return make_response(jsonify(errors), ERROR)

        term = Terms(**json_data)
        db.session.add(term)
        db.session.commit()
        term_schema = TermsSchema()
        data = term_schema.dump(Terms.query.get(term.id))
        return make_response(jsonify(data), CREATED_STATUS_CODE)
    except marshmallow.ValidationError as errors:
        return make_response(jsonify(errors.messages), ERROR)

