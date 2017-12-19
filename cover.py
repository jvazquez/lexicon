# -*- coding: utf-8 -*-
"""
:mod:`cover` -- Handle the configuration of coverage
===================================

.. module:: cover
   :platform: Unix, Windows
   :synopsis: Enable the coverage api
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""

import os
import coverage

if os.getenv('MANUALCOV', False):
    COV = coverage.coverage()
    COV.start()
