# hex.py
#
# Defines the attributes of the Hex class


class Hex:

    def __init__(self, hex_map, master, parent, id, hex_menu_callback, row, column, adjacent_coords, ring_number):
        self._master = master
        self._parent = parent
        self._hex_map_ref = hex_map
        self._hex_menu_callback = hex_menu_callback
        self._owner = None
        self._id = id
        self._coords = (row, column)
        self._adjacent_coords = adjacent_coords
        self._ring_number = ring_number
        self._structure_coords = None
        self._structure_id = None
        self._adjacent_ids = self.set_adjacent_ids(parent, adjacent_coords)
        self._squad_slot_ids = [None, None]
        self._squad_slot_coords = None
        self._res_value = 25
        self._structure = "None"
        self._squad_1 = None
        self._squad_2 = None

        hex_map.tag_bind(self._id, "<Button-1>", self.show_hex_menu)

    def show_hex_menu(self, event=None):
        self._hex_menu_callback(self)

        # Grey/black hex toggle code:

        # if self._owner == "None":
        #     event.widget.itemconfig(self._id, fill="gray")
        #     self._owner = "Block"
        # elif self._owner == "Block":
        #     event.widget.itemconfig(self._id, fill="black")
        #     self._owner = "None"


    def get_id(self):
        return self._id

    def get_owner(self):
        return self._owner

    def get_owner_name_str(self):
        if self._owner is None:
            return "None"
        else:
            return self._owner.get_name()

    def get_value(self):
        return self._res_value

    def set_value(self, new_value):
        self._res_value = new_value

    def get_vp_value(self):
        if self._structure != "None":
            if self._structure == "Mine":
                return self._ring_number + 1
            elif self._structure == "Refinery":
                return self._ring_number + 5
        return self._ring_number

    def get_ring_depth(self):
        return self._ring_number

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
        # FIXME: Refactor protected variable access
        id_list = []
        for coords in coord_list:
            id_list.append(parent._coords_to_id(coords))
        return id_list

    def get_adjacent_ids(self):
        return self._adjacent_ids

    def check_if_squad_present(self):
        if self._squad_1 is not None or self._squad_2 is not None:
            return True
        else:
            return False

    def check_open_space(self):
        if self._squad_1 is None or self._squad_2 is None:
            return True
        else:
            return False

    def set_squad_slot_ids(self, id_list):
        self._squad_slot_ids = id_list

    def set_squad_slot_coords(self, coords):
        self._squad_slot_coords = coords

    def get_squad_slots(self):
        return self._squad_slot_ids

    def get_squads(self):
        squad_list = []
        if self._squad_1 is not None:
            squad_list.append(self._squad_1)
        if self._squad_2 is not None:
            squad_list.append(self._squad_2)
        return squad_list

    # def get_first_open_slot(self):
    #     if self._squad_1 is None:
    #         return self._squad_slot_ids[0]
    #     elif self._squad_2 is None:
    #         return self._squad_slot_ids[1]
    #     else:
    #         return None

    def get_first_open_slot(self):
        if self._squad_1 is None:
            return self._squad_slot_coords[0]
        elif self._squad_2 is None:
            return self._squad_slot_coords[1]
        else:
            return None

    # def add_squad(self, squad):
    #     if self._squad_1 is None:
    #         self._squad_1 = squad
    #         self._hex_map_ref.itemconfig(self._squad_slot_ids[0], window=squad.get_squad_icon())
    #         return self._squad_slot_ids[0]
    #     elif self._squad_2 is None:
    #         self._squad_2 = squad
    #         self._hex_map_ref.itemconfig(self._squad_slot_ids[1], window=squad.get_squad_icon())
    #         return self._squad_slot_ids[1]
    #     else:
    #         #FIXME: Add error processing for full hex
    #         print("Hex is full, can't add")
    #         return

    def add_squad(self, squad):
        if self._squad_1 is None:
            self._squad_1 = squad
            self._squad_slot_ids[0] = self._hex_map_ref.create_window(self._squad_slot_coords[0][0],
                                                                      self._squad_slot_coords[0][1])
            squad.set_squad_slot_id(self._squad_slot_ids[0])
            self._hex_map_ref.itemconfig(self._squad_slot_ids[0], window=squad.get_squad_icon())
            return self._squad_slot_ids[0]
        elif self._squad_2 is None:
            self._squad_2 = squad
            self._squad_slot_ids[1] = self._hex_map_ref.create_window(self._squad_slot_coords[1][0],
                                                                      self._squad_slot_coords[1][1])
            squad.set_squad_slot_id(self._squad_slot_ids[1])
            self._hex_map_ref.itemconfig(self._squad_slot_ids[1], window=squad.get_squad_icon())
            return self._squad_slot_ids[1]
        else:
            #FIXME: Add error processing for full hex
            print("Hex is full, can't add")
            return

    # def remove_squad(self, squad_slot_id):
    #     print("Removing squad...")
    #     if squad_slot_id == self._squad_slot_ids[0]:
    #         print("Clearing reference from slot " + str(self._squad_slot_ids[0]))
    #         self._squad_1 = None
    #         # self._hex_map_ref.itemconfig(squad_slot_id, window=None)
    #         self._hex_map_ref.delete(squad_slot_id)
    #     elif squad_slot_id == self._squad_slot_ids[1]:
    #         print("Clearing reference from slot " + str(self._squad_slot_ids[1]))
    #         self._squad_2 = None
    #         # self._hex_map_ref.itemconfig(squad_slot_id, window=None)
    #         self._hex_map_ref.delete(squad_slot_id)

    def remove_squad(self, squad_slot_id):
        print("Removing squad...")
        if squad_slot_id == self._squad_slot_ids[0]:
            print("Clearing reference from slot " + str(self._squad_slot_ids[0]))
            self._squad_1 = None
            self._squad_slot_ids[0] = None
            self._hex_map_ref.delete(squad_slot_id)
        elif squad_slot_id == self._squad_slot_ids[1]:
            print("Clearing reference from slot " + str(self._squad_slot_ids[1]))
            self._squad_2 = None
            self._squad_slot_ids[1] = None
            self._hex_map_ref.delete(squad_slot_id)

    def change_owner(self, player, colour):
        self._owner = player
        self._parent.hex_grid.itemconfig(self._id, fill=colour)

