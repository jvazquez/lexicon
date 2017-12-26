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
CREATED_RELATED_TERM = 201
DELETED = 200
ERROR = 400
FOUND = 200
MISSING_PAYLOAD = _('No input data provided.')
NOT_FOUND = 404
OK = 200
PING_RESPONSE_TEXT = _('I am alive.')
UNSUPPORTED_MEDIA = 415
UPDATED = 200
RELATED_TERM_CREATED = _('Related term created.')
RELATED_TERM_NOT_FOUND = _('Related term not found.')
RELATED_TERMS_FOUND = _('Related terms found.')
TERM_FOUND = _('Term found.')
TERMS_FOUND = _('Term found.')
TERM_NOT_FOUND = _('Requested term not found.')
TERM_DELETED = _('Term deleted.')
TERM_UPDATED = _('Term updated.')
