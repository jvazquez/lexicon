# -*- coding: utf-8 -*-
"""
:mod:`tests` -- Several test cases
===================================

.. module:: tests
   :platform: Unix, Windows
   :synopsis: Set of unit tests and functional tests.
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import logging
import os

import log_config

logger = logging.getLogger(__name__)

os['CONFIGURATION'] = 'testing'

