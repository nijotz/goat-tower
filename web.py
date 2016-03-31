import random
import re
import uuid
from flask import abort, Flask, jsonify, request, send_from_directory
from goattower import db, engine, init
from goattower.models import Actor, User


app = Flask(__name__, static_url_path='', static_folder='web')


def create_name():
    return 'WebUser{:05d}'.format(random.randint(1,99999))

def verify_name(name):
    return re.match('WebUser[0-9]{5}', name) is not None


def create_user(name):
    actor = Actor(name=name)
    actor.parent_id = 1
    db.session.add(actor)
    db.session.commit()
    user = User(name=name)
    user.actor_id = actor.id
    db.session.add(user)
    db.session.commit()
    return user


def do_goat_things(name, command):
    user = db.session.query(User).filter(User.name == name).first()
    if not user:
        user = create_user(name)

    engine.handle_text(user.actor.id, command)

    return engine.get_text(user.actor.id)


@app.route('/api', methods=['POST'])
def api():
    if not (request.json or 'command' in request.json):
        abort(400)

    if not 'user' in request.json:
        username = create_name()
    else:
        username = request.json['user']

    if not verify_name(username):
        abort(400)

    command = request.json['command']
    result = do_goat_things(username, command)
    return jsonify( {'user': username, 'result': result} )


if __name__ == '__main__':
    init()
    app.run(debug=True)
