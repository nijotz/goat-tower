import logging
import json
import sys
from sqlalchemy.orm import sessionmaker
import models


logger = logging.getLogger('goattower.load')

# For some reason, I can't just commit at the end of this loop.  It will
# randomly try to insert a command that foreign keys to an actor that isn't
# inserted yet, despite the loop adding objects to the sesion in the right
# order.  To fix, I just commit after every add.
def load_data(data):
    from models import engine
    Session = sessionmaker(bind=engine)
    session = Session()
    models.init_db()

    for actor in data:
        new_actor = models.Actor(name=actor['name'])
        parent_name = actor.get('parent', None)
        if parent_name:
            parent = session.query(models.Actor).filter(models.Actor.name == parent_name).one()
            new_actor.parent_id = parent.id
        logger.debug('Adding actor: {}'.format(new_actor.name))
        session.add(new_actor)
        session.commit()

        for command in actor.get('commands', []):
            commands = []
            for regex in command['regex']:
                new_command = models.Command(
                    regex=regex,
                    actor_id=new_actor.id)
                commands.append(new_command)
                logger.debug('Adding command: {}'.format(new_command.regex))
                session.add(new_command)
                session.commit()

            code = []
            for command in command['code']:
                method, args = command.popitem()
                new_code = models.Code(method, json.dumps(args))
                code.append(new_code)
                logger.debug('Adding code: {} {}'.format(new_code.method, new_code.args))
                session.add(new_code)
                session.commit()

            for command in commands:
                for cd in code:
                    command.code.append(cd)
            session.commit()

        for key, value in actor.get('attributes', {}).iteritems():
            new_attr = models.Attribute(
                actor_id=new_actor.id,
                key=key,
                value=value)
            logger.debug('Adding attribute: {} - {}'.format(new_attr.key, new_attr.value))
            session.add(new_attr)
            session.commit()


def load_json(json_str):
    load_data(json.loads(json_str))

def load_yaml(yaml_str):
    import yaml
    load_data(yaml.load(yaml_str))

parser_map = {
    'yaml': load_yaml,
    'json': load_json,
}

def load(data_file, data_type):
    parser = parser_map.get(data_type, None)
    parser(open(data_file).read())

def main():
    import argparse
    argparse # TODO: eventually..

    data_file = sys.argv[1]
    file_type = sys.argv[2]
    parser = parser_map.get(file_type, None)
    if parser:
        parser(open(data_file).read())
    else:
        print 'File type "{}" not supported'.format(file_type)
        sys.exit(1)

if __name__ == '__main__':
    main()
