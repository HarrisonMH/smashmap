# squad.py
#
# Defines attributes of a squad

class Squad():

    def __init__(self, owner, fighter, location, create_squad_icon_callback):
        self._create_squad_icon_callback = create_squad_icon_callback
        self._squad_icon = None
        self._squad_slot_id = None
        self._owner = owner
        self._fighter = fighter
        self._kills = 0
        self._hex_location = location
        # self._create_squad_icon_callback(self._hex_location, self._fighter, self._set_squad_icon_callback)
        self._create_squad_icon_callback(self)

        self._turn_taken = False


    def get_owner_name(self):
        return self._owner.get_name()

    def get_owner(self):
        return self._owner

    def get_fighter(self):
        return self._fighter

    def get_kills(self):
        return self._kills

    def increment_kills(self):
        self._kills += 1
        return

    def get_turn_status(self):
        return self._turn_taken

    def get_location(self):
        return self._hex_location

    def get_squad_icon(self):
        return self._squad_icon

    def set_location(self, new_loc):
        self._hex_location = new_loc

    def get_squad_id(self):
        return self._squad_icon

    def set_squad_icon(self, icon_reference, squad_slot_id):
        self._squad_icon = icon_reference
        self._squad_slot_id = squad_slot_id
        self._squad_icon.bind("<Button-1>", self._map_icon_click)

    def move_squad(self, event, hex_map_ref):
        new_loc = int(event.widget.cget("text"))
        hex_list = hex_map_ref.get_hex_list()
        hex_list[self._hex_location - 1].remove_squad(self._squad_slot_id)
        # self._squad_slot_id = hex_list[new_loc - 1].add_squad(self._squad_icon)
        self._squad_slot_id = hex_list[new_loc - 1].add_squad(self)
        if hex_list[new_loc - 1].get_owner() != self._owner.get_name():
            hex_list[new_loc - 1].change_owner("None", "white")

        self.set_location(new_loc)

    def _map_icon_click(self, event):
        print("Map icon: " + self._fighter)
        # self._squad_icon.config(state="disabled")

