import unittest
import coverage

from flask_script import Manager
from api import create_app

# code coverage
COV = coverage.coverage(
    branch=True,
    include='api/*',
    omit=[
        'tests/*',
        'api/config.py',
        'api/*/__init__.py'
    ]
)
COV.start()

app = create_app()
manager = Manager(app)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
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


if __name__ == '__main__':
    manager.run()

