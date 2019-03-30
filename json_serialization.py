import json

jsonClasses = []

def json_class(klass):
    jsonClasses.append(klass)
    return klass

class CustomDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if '__class__' not in obj:
            return obj
        type = obj['__class__']

        for klass in jsonClasses:
            if type == klass.__name__:
                return klass(**obj)
        return obj

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        for klass in jsonClasses:
            if isinstance(obj, klass):
                cpy = obj.__dict__.copy()
                cpy["__class__"] = obj.__class__.__name__
                return cpy
        return json.JSONEncoder.default(self, obj)

def load_gamedata(savefile):
    with open(savefile, "r") as f:
        return json.load(f, cls=CustomDecoder)

def save_gamedata(gamedata, savefile):
    with open(savefile, "w") as f:
        json.dump(gamedata, f, cls=CustomEncoder, indent=2)
