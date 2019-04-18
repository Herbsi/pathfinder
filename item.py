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
        return "{:+d} {ia} when {uh}".format(
            self.amount, ia=self.influenced_attribute, uh=used_held
        )
