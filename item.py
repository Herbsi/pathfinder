from json_serialization import json_class


@json_class
class Item:
    def __init__(self, **item):
        self.name = ""
        self.price = 0
        self.influenced_attribute = ""
        self.amount = 0
        self.passive_effect = False
        self.__dict__.update(item)

    @property
    def effect(self):
        used_held = "held" if self.passive_effect else "used"
        if self.amount > 0:
            return "(+{} {} when {})".format(self.amount, self.influenced_attribute, used_held)
        else:
            return "({} {} when {})".format(self.amount, self.influenced_attribute, used_held)
