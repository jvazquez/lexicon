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

from app import db
from terms.models import Terms, RelatedTerms


class TermsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Terms
        sqlalchemy_session = db.session
    id = factory.Sequence(lambda n: n + 1)
    word = factory.Sequence(lambda n: u'Word {}'.format(n))
    definition = factory.Sequence(lambda n: u'Definition {}'.format(n))


class RelatedTermsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = RelatedTerms
        sqlalchemy_session = db.session
    id = factory.Sequence(lambda n: n + 1)
    term = factory.SubFactory(TermsFactory)
    related_term = factory.SubFactory(TermsFactory)
