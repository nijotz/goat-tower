from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


class Database(object):

    def init(self, uri):
        self.engine = create_engine(uri)
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(self.engine)
