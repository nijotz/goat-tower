import re
from unittest import TestCase

import pexpect

from goattower import db, engine, init, settings
from goattower.models import Base
from goattower.load import load


class BaseTestCase(TestCase):

    def setUp(self):
        settings.TESTING = True
        init()
        Base.metadata.drop_all(db.engine)
        Base.metadata.create_all(db.engine)
        load('goattower/tests/fixtures/story.yaml', 'yaml', db.session)


class APIfTestCase(BaseTestCase):

    def test_api_script(self):
        script = open('goattower/tests/fixtures/story.scr')
        for line in script:
            line = line.rstrip()
            if line.startswith('>>> '):
                while engine.get_text(3):
                    pass
                engine.handle_text(3, line.replace('>>> ', ''))
            else:
                text = engine.get_text(3)[0]
                self.assertIsNotNone(re.match(line, text))


class REPLTestCase(BaseTestCase):

    def test_repl_script(self):
        script = open('goattower/tests/fixtures/story.scr')
        repl = pexpect.spawn('goattower/scripts/repl.sh 3', timeout=5)
        for line in script:
            line = line.rstrip()
            if line.startswith('>>> '):
                repl.expect('baaa> ')
                repl.sendline(line.replace('>>> ', ''))
            else:
                repl.expect(line)
