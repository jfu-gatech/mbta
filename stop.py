import json

class Stop:
    """
    models MBTA's Stop endpoint
    https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index
    """
    def __init__(self, id, attributes, links, relationships, type):
        self.id = id
        self.name = attributes["name"] if "name" in attributes else None

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
