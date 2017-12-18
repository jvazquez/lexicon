# -*- coding: utf-8 -*-
"""
:mod:`models` -- Models for the terms
===================================

.. module:: models
   :platform: Unix, Windows
   :synopsis: Handles the flask-sqlalchemy models
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import gettext

from marshmallow import Schema, fields, validates, validate, ValidationError

from api import db
from api.constants import ERROR


_ = gettext.gettext


class Terms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.Unicode(length=100), index=True, unique=True)
    definition = db.Column(db.UnicodeText(), nullable=False)
    created = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, nullable=True)


class RelatedTerms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=False)
    related_term_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, nullable=True)


def not_an_space(word):
    """
    Validates that the provided word is not a single space
    Parameters:
        word `str`
    Raises
        ValidationError
    """

    if word.isspace():
        raise ValidationError('Word cannot be a space')


class TermsSchema(Schema):
    id = fields.Int(dump_only=True)
    word = fields.String(required=_('Please provide a valid term'),
                         validate=[validate.Length(min=1,
                                                   max=100,
                                                   error=(
                                                       'Word must be greater'
                                                       'than 1 and lower or '
                                                       'equal to 100 characters'
                                                   )
                                                ),

                                   not_an_space]
                         )
    definition = fields.String(required=True, validate=[validate.Length(min=1), not_an_space])
    created = fields.DateTime(requred=False)
    updated = fields.DateTime(requred=False)

