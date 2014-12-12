import json
import re
from jinja2 import Environment
from models import Actor, Attribute, PlayerText


def get_actor_id_by_name(name):
    # TODO needs to filter by location as well to support say to actor
    # at my location
    return 4

def from_json(json_str):
    return json.loads(json_str)


class API(object):

    def __init__(self):
        self.environment = Environment()
        self.environment.filters['get_actor_id_by_name'] = get_actor_id_by_name
        self.environment.filters['fromjson'] = from_json

    def init(self, session):
        self.session = session

    def run_method(self, method_name, args_string, context):
        template = self.environment.from_string(args_string)
        args_json_string = template.render(context)
        getattr(self, method_name)(*json.loads(args_json_string), context=context)

    def inc_attr(self, actor_name, attribute, context):
        actor = self.session.query(Actor).filter(Actor.name == actor_name).one()
        attribute = self.session.query(Attribute).filter(Attribute.actor_id == actor.id).one()
        attribute.value = int(attribute.value) + 1
        self.session.commit()

    def send_text(self, actor_id, text, context):
        actor = self.session.query(Actor).get(actor_id)
        if actor.is_player:
            self.session.add(PlayerText(actor_id, text))
            self.session.commit()
        else:
            # TODO: this is copied from engine, which sucks.  The only
            # difference is that context['origin'] is passed to run_code
            from engine import command_queries
            commands = command_queries['character'].params(actor_id=actor_id).all()
            matches = []
            for command in commands:
                regex = re.compile(command.regex).match
                match = regex(text)
                if match:
                    matches.append((command, match))
            if len(matches) > 1:
                print 'Ambiguous command'
                return
            elif len(matches) == 1:
                from engine import run_code
                run_code(context['origin'], *matches[0])
                return

    def update_location(self, actor_id, location, context):
        actor = self.session.query(Actor).get(actor_id)
        location = self.session.query(Actor).filter(Actor.name == location).one()
        actor.parent_id = location.id
        self.session.commit()

    def append_attr_json(self, actor_name, attribute, item, context):
        actor = self.session.query(Actor).filter(Actor.name == actor_name).one()
        attribute = self.session.query(Attribute).filter(Attribute.actor_id == actor.id).one()
        attr_json = json.loads(attribute.value)
        attr_json.append(item)
        attribute.value = json.dumps(attr_json)
        self.session.commit()
