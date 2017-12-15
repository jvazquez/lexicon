# -*- coding: utf-8 -*-
"""
:mod:`endpoints` -- Endpoints for the terms application
===================================

.. module:: endpoints
   :platform: Unix, Windows
   :synopsis: Handles the several endpoints of terms
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
from flask import Blueprint

import models

terms_bp = Blueprint('terms', __name__)


@terms_bp.route('/', methods=['GET'])
def get_all_terms():
    pass

