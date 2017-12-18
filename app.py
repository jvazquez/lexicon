# -*- coding: utf-8 -*-
"""
:mod:`module-name` -- description
===================================

.. module:: module-name
   :platform: Unix, Windows
   :synopsis: complete
.. moduleauthor:: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import coverage
import os
import unittest

from flask import Flask
from flask_bcrypt import Bcrypt
from orm import db
from terms.endpoints import terms_bp

app = Flask(__name__)
configuration = os.getenv('CONFIGURATION', 'development')
config_dir = os.path.abspath(os.path.dirname(__file__))
app.config.from_pyfile('configuration/{}.py'.format(configuration))
db.init_app(app)
bcrypt = Bcrypt(app)
app.register_blueprint(terms_bp)


@app.cli.command(with_appcontext=False)
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@app.cli.command(with_appcontext=False)
def cov():
    """Runs the unit tests with coverage."""
    COV = coverage.coverage()
    COV.start()
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1
