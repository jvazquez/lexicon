# -*- coding: utf-8 -*-
"""
:mod:`endpoints` -- Endpoints for the terms application
===================================

.. module:: endpoints
   :platform: Unix, Windows
   :synopsis: Handles the several endpoints of terms
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
from flask import Blueprint, jsonify, make_response, request

from api.constants import CREATED_STATUS_CODE, ERROR
from api.terms.models import Terms
from api.terms.validators import ValidateCreate

terms_bp = Blueprint('terms', __name__)


@terms_bp.route('/', methods=['POST'])
def create_term():
    data = request.json

    if data is None:
        return make_response(jsonify({}), ERROR)

    validator = ValidateCreate(data)
    if validator.valid():
        pass
    else:
        return make_response(jsonify({}), ERROR)

