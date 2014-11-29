import re
from unittest import TestCase

from sqlalchemy import create_engine

from goattower import models
from goattower.engine import get_text, handle_text
from goattower.models import Base
from goattower.load import load


class BaseTestCase(TestCase):

    def setUp(self):
        engine = create_engine('postgresql+psycopg2://@/goattower-tests')
        models.engine = engine
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        load('goattower/tests/fixtures/story.yaml', 'yaml')


class APIfTestCase(BaseTestCase):

    def test_api_script(self):
        return  #TODO: fix, test database is being used by pexpect command
        script = open('goattower/tests/fixtures/story.scr')
        for line in script:
            line = line.rstrip()
            if line.startswith('>>> '):
                handle_text(line.replace('>>> ', ''))
            else:
                self.assertIsNotNone(re.match(line, get_text(3)))

'''
class REPLTestCase(BaseTestCase):

    def test_repl_script(self):
        return  #TODO: fix, test database is being used by pexpect command
        script = open('goattower/tests/fixtures/story.scr')
        repl = pexpect.spawn('goattower/scripts/repl.sh 3', timeout=5)
        for line in script:
            line = line.rstrip()
            if line.startswith('>>> '):
                repl.expect('baaa> ')
                repl.sendline(line.replace('>>> ', ''))
            else:
                repl.expect(line)
'''
