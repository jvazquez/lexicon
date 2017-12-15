# -*- coding: utf-8 -*-
"""
:mod:`api` -- Lexicon access 
===================================

.. module:: api
   :platform: Unix, Windows
   :synopsis: Crud for terms.
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def create_app():
    """Creates a flask application
    Returns:
        flask.  The configured flask application
    """

    app = Flask(__name__)
    configuration = os.getenv('CONFIGURATION', 'development')
    config_dir = os.path.abspath(os.path.dirname(__file__))
    app.config.from_pyfile('{}/configuration/{}.py'.format(config_dir, configuration))
    return app

