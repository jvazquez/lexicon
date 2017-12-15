# -*- coding: utf-8 -*-
"""
:mod:`models` -- Models for the terms
===================================

.. module:: models
   :platform: Unix, Windows
   :synopsis: Handles the flask-sqlalchemy models
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
from lexicon.api import db


class Terms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.Unicode(length=100), index=True)
    definition = db.Column(db.UnicodeText(), nullable=False)
    created = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, nullable=True)


class RelatedTerms(db.Model):
    term_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=False)
    related_term_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, nullable=True)

