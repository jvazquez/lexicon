# -*- coding: utf-8 -*-
"""
:mod:`module-name-here` -- Description here 
===================================

.. module:: module-name-here
   :platform: Unix, Windows
   :synopsis: complete.
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import os

from collections import deque

import logconfig

if os.path.exists('logging.json'):
    __config = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'logging.json')
    logconfig.from_file(__config)

