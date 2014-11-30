import re

from sqlalchemy.orm import aliased
from sqlalchemy.sql import bindparam

from models import Actor, Command, PlayerText


class Engine(object):

    def init(self, session, api):
        self.session = session
        self.api = api

        # compile queries
        self.command_queries = {}
        self.command_queries['character'] = \
            session.query(Command).\
            filter(Command.actor_id == bindparam('actor_id'))

        self.command_queries['children'] = \
            session.query(Actor, Command).\
            filter(Actor.id == bindparam('actor_id')).\
            join(Actor.parent, aliased=True).\
            filter(Command.actor_id == Actor.id)

        location = aliased(Actor)
        self.command_queries['location'] = \
            session.query(Command).\
            join(location).\
            join(Actor, location.id == Actor.parent_id).\
            filter(Actor.id == bindparam('actor_id'))

        location = aliased(Actor)
        children = aliased(Actor)
        self.command_queries['location_children'] = \
            session.query(Command).\
            join(children).\
            join(location, location.id == children.parent_id).\
            join(Actor, location.id == Actor.parent_id).\
            filter(Actor.id == bindparam('actor_id')).\
            filter(Command.actor_id == children.id)

        self.command_precedence = ['character', 'children', 'location', 'location_children']

    def handle_text(self, actor_id, text):
        # TODO: have some game commands
        # For now assume all text is intended for a game object

        #TODO: FUCKING COMMENT
        for command_type in self.command_precedence:
            commands = self.command_queries[command_type].params(actor_id=actor_id).all()
            matches = []
            for command in commands:
                regex = re.compile(command.regex).match
                match = regex(text)
                if match:
                    matches.append((command, match))

            if len(matches) > 1:
                # Too many matches, ambiguous
                self.api.send_text(actor_id, 'Ambiguous command')
                return
            elif len(matches) == 1:
                # Exactly one match, respond
                self.run_code(actor_id, *matches[0])
                return

        class fake_matchgroup(object):
            def groupdict(self):
                return

        # We have no matches, just shout at user
        self.api.send_text(actor_id, 'Huh?', fake_matchgroup())

    def get_text(self, actor_id):
        text_objs = self.session.query(PlayerText).\
            filter(PlayerText.actor_id == actor_id)
        text = []
        for text_obj in text_objs:
            text.append(text_obj.text)
            self.session.delete(text_obj)
        self.session.commit()
        return text

    def run_code(self, actor_id, command, match):
        context = {
            'origin': actor_id,
            'match': match.groupdict(),
            'actor': command.actor
        }
        for code in command.code:
            self.api.run_method(code.method, code.args, context)
