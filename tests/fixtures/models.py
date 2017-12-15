# -*- coding: utf-8 -*-
"""
:mod:`module-name-here` -- Description here 
===================================

.. module:: module-name-here
   :platform: Unix, Windows
   :synopsis: complete.
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import factory

from api.terms.models import Terms, RelatedTerms


class TermsFactory(factory.Factory):
    class Meta:
        model = Terms


class RelatedTermsFactory(factory.Factory):
    class Meta:
        model = RelatedTerms

