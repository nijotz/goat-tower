import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))
from goattower import db, engine, init, models

init()

actor = db.session.query(models.Actor).filter(models.Actor.name == sys.argv[1]).one()
command = ' '.join(sys.argv[2:])
engine.handle_text(actor.id, command)
for text in engine.get_text(actor.id):
    print text
