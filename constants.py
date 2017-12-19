# -*- coding: utf-8 -*-
"""
:mod:`module-name-here` -- Description here 
===================================

.. module:: module-name-here
   :platform: Unix, Windows
   :synopsis: complete.
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import gettext

_ = gettext.gettext

CREATED_STATUS_CODE = 201
DELETED = 200
ERROR = 400
NOT_FOUND = 404
UNSUPPORTED_MEDIA = 415
MISSING_PAYLOAD = _('No input data provided.')
TERM_NOT_FOUND = _('Requested term not found.')
TERM_DELETED = _('Term deleted.')