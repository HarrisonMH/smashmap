# hex.py
#
# Defines the attributes of the Hex class


class Hex():

    def __init__(self, hex_map, master, parent, id, hex_menu_callback, row, column, adjacent_coords):
        self._master = master
        self._parent = parent
        self._hex_map_ref = hex_map
        self._hex_menu_callback = hex_menu_callback
        self._owner = "None"
        self._id = id
        self._coords = (row, column)
        self._adjacent_coords = adjacent_coords
        self._structure_coords = None
        self._structure_id = None
        self._adjacent_ids = self.set_adjacent_ids(parent, adjacent_coords)
        self._squad_slot_ids = None
        self._value = 25
        self._structure = "None"
        self._squad_1 = None
        self._squad_2 = None

        hex_map.tag_bind(self._id, "<Button-1>", self._show_menu)


    def _show_menu(self, event=None):
        self._hex_menu_callback(self._master, self)

        # Grey/black hex toggle code:

        # if self._owner == "None":
        #     event.widget.itemconfig(self._id, fill="gray")
        #     self._owner = "Block"
        # elif self._owner == "Block":
        #     event.widget.itemconfig(self._id, fill="black")
        #     self._owner = "None"


    def get_id(self):
        # print(self._id)
        return self._id

    def get_owner(self):
        return self._owner

    def get_structure(self):
        return self._structure

    def set_structure(self, structure, hex_map_create_structure_callback):
        self._structure = structure
        hex_map_create_structure_callback(self, structure)

    def set_structure_coords(self, coords):
        self._structure_coords = coords

    def get_structure_coords(self):
        return self._structure_coords

    def set_structure_id(self, id):
        self._structure_id = id

    def get_structure_id(self):
        return self._structure_id

    def get_coords(self):
        return self._coords

    def get_adjacency_coords(self):
        return self._adjacent_coords

    def set_adjacent_ids(self, parent, coord_list):
        id_list = []
        for coords in coord_list:
            id_list.append(parent._coords_to_id(coords))
        return id_list

    def get_adjacent_ids(self):
        return self._adjacent_ids

    def check_open_space(self):
        if self._squad_1 == None or self._squad_2 == None:
            return True
        else:
            return False

    def set_squad_slot_ids(self, id_list):
        self._squad_slot_ids = id_list

    def get_squad_slots(self):
        return self._squad_slot_ids

    def get_squads(self):
        return [self._squad_1, self._squad_2]

    def get_first_open_slot(self):
        if self._squad_1 == None:
            return self._squad_slot_ids[0]
        else:
            return self._squad_slot_ids[1]

    def add_squad(self, squad):
        if self._squad_1 == None:
            self._squad_1 = squad
            self._hex_map_ref.itemconfig(self._squad_slot_ids[0], window=squad.get_squad_icon())
            return self._squad_slot_ids[0]
        else:
            if self._squad_2 == None:
                self._squad_2 = squad
                self._hex_map_ref.itemconfig(self._squad_slot_ids[1], window=squad.get_squad_icon())
                return self._squad_slot_ids[1]
            else:
                #FIXME: Add error processing for full hex
                print("Hex is full, can't add")

    def remove_squad(self, squad_slot_id):
        print("Removing squad...")
        if squad_slot_id == self._squad_slot_ids[0]:
            print("Clearing reference from slot " + str(self._squad_slot_ids[0]))
            self._squad_1 = None
            self._hex_map_ref.itemconfig(squad_slot_id, window=None)
        elif squad_slot_id == self._squad_slot_ids[1]:
            print("Clearing reference from slot " + str(self._squad_slot_ids[0]))
            self._squad_2 = None
            self._hex_map_ref.itemconfig(squad_slot_id, window=None)

    def change_owner(self, name, colour):
        self._owner = name
        self._parent.hex_grid.itemconfig(self._id, fill=colour)

        #FIXME: Pass Player object into method instead of attributes
        # self._owner = player
        # self._parent.hex_grid.itemconfig(self._id, fill=player.get_colour())

