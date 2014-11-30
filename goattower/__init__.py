from api import API
from database import Database
from engine import Engine
import settings


db = Database()
engine = Engine()
api = API()


def init():
    if getattr(settings, 'TESTING', None):
        uri = settings.TEST_DB_URI
    else:
        uri = settings.DB_URI
    db.init(uri)
    engine.init(db.session, api)
    api.init(db.session)
