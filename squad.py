# squad.py
#
# Defines attributes of a squad


class Squad:

    def __init__(self, owner, fighter, location, create_squad_icon_callback, battle_popup_callback,
                 set_selected_squad_callback, get_selected_squad_callback, get_current_player_callback):
        self._create_squad_icon_callback = create_squad_icon_callback
        self._battle_popup_callback = battle_popup_callback
        self._set_selected_squad_callback = set_selected_squad_callback
        self._get_selected_squad_callback = get_selected_squad_callback
        self._get_current_player_callback = get_current_player_callback
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

    def take_turn(self):
        self._turn_taken = True
        self._squad_icon.config(state="disabled")

    def refresh_turn(self):
        self._turn_taken = False
        self._squad_icon.config(state="normal")

    def get_turn_status(self):
        return self._turn_taken

    def get_location(self):
        return self._hex_location

    def get_squad_icon(self):
        return self._squad_icon

    def set_location(self, new_loc):
        self._hex_location = new_loc

    def get_squad_slot_id(self):
        return self._squad_slot_id

    def set_squad_slot_id(self, new_id):
        self._squad_slot_id = new_id

    # def set_squad_icon(self, icon_reference, squad_slot_id):
    #     self._squad_icon = icon_reference
    #     self._squad_slot_id = squad_slot_id
    #     self._squad_icon.bind("<Button-1>", self._map_icon_click)

    def set_squad_icon(self, icon_reference):
        self._squad_icon = icon_reference
        self._squad_icon.bind("<Button-1>", self._map_icon_click)
        self._squad_icon.bind("<Button-3>", self._map_icon_right_click)

    def move_squad(self, new_loc_id, hex_map_ref, parent_menu_str):
        # new_loc_id = int(event.widget.cget("text"))
        hex_list = hex_map_ref.get_hex_list()
        new_loc_hex = hex_list[new_loc_id - 1]
        # print("Hex " + str(new_loc_hex.get_id()) + " occupied: " + str(new_loc_hex.check_if_squad_present()))
        if self.check_hex_for_enemy(new_loc_hex) is True and new_loc_hex.get_structure() != "HQ":
            self._battle_popup_callback(self, new_loc_hex)
        elif new_loc_hex.check_open_space() is True:
            if new_loc_hex.get_structure() != "HQ" and new_loc_hex.get_owner != self._owner:
                # hex_map_ref.hex_grid.tag_lower(self._squad_slot_id)
                self._hex_location.unhighlight_adjacent_hexes()
                self._hex_location.remove_squad(self._squad_slot_id)
                new_loc_hex.add_squad(self)
                if new_loc_hex.get_owner() != self._owner and new_loc_hex.get_owner() is not None:
                    new_loc_hex.get_owner().adjust_territory_size(-1)
                    new_loc_hex.get_owner().adjust_income(new_loc_hex.get_value() * -1)
                    new_loc_hex.get_owner().adjust_vp_income(new_loc_hex.get_vp_value() * -1)
                    new_loc_hex.change_owner(None, "white")
                self.take_turn()
                self.refresh_active_menu(parent_menu_str)
                self.set_location(new_loc_hex)
                self.deselect_squad()
            else:
                print("Cannot move into enemy HQ")
        else:
            print("Can't move to this position: hex is full")

    def destroy_squad(self, parent_menu_str):
        print("Deleting squad in slot: ", self._squad_slot_id)
        self.deselect_squad()
        self.get_location().unhighlight_adjacent_hexes()
        self._squad_icon = None
        self._hex_location.remove_squad(self._squad_slot_id)
        self._owner.destroy_squad(self)
        self.refresh_active_menu(parent_menu_str)

    def _map_icon_click(self, event):
        # print("Map icon: ", self._fighter, " in slot ", self._squad_slot_id)
        # FIXME: Add deselection logic when clicking on a selected squad
        if self._get_current_player_callback() == self._owner:
            current_selected_squad = self._get_selected_squad_callback()
            if current_selected_squad == self:
                self.deselect_squad()
                self._hex_location.unhighlight_adjacent_hexes()
            else:
                if current_selected_squad is not None and current_selected_squad != self:
                    self._get_selected_squad_callback().get_location().unhighlight_adjacent_hexes()
                icon_state = self._squad_icon.cget("state")
                if icon_state != "disabled" and icon_state != "active":
                    self._squad_icon.config(state="active")
                    self._set_selected_squad_callback(self)
                    self._hex_location.highlight_adjacent_hexes()
        else:
            print("Cannot select enemy squad")

    def _map_icon_right_click(self, event):
        if self._get_current_player_callback() == self._owner:
            current_selected_squad = self._get_selected_squad_callback()
            if current_selected_squad == self:
                print("Right click on selected squad!")
                self._hex_location._parent.squad_context_menu(self)


    def deselect_squad(self):
        if self._squad_icon.cget("state") != "disabled":
            self._squad_icon.config(state="normal")
        self._set_selected_squad_callback(None)

    def refresh_active_menu(self, active_menu_str):
        """Takes the name of the active menu in string format and invokes the callback to refresh the active menu."""
        if active_menu_str == "player":
            print("Refreshing player menu")
            self._owner.show_player_menu()
        elif active_menu_str == "hex":
            print("Refreshing hex menu")
            self._hex_location.show_hex_menu()

    def check_hex_for_enemy(self, hex):
        if hex.check_if_squad_present() is True:
            enemy_squads = hex.get_squads()
            for squad in enemy_squads:
                if squad.get_owner() != self._owner:
                    return True
        return False

    def colonize(self):
        print("Owner of hex", self._hex_location.get_id(), ": ", self._hex_location.get_owner())
        if self._hex_location.get_owner() is None:
            self._hex_location.change_owner(self._owner, self._owner.get_colour())
            self.take_turn()
            self._owner.adjust_territory_size(1)
            self._owner.adjust_income(self._hex_location.get_value())
            self._owner.adjust_vp_income(self._hex_location.get_vp_value())
            # FIXME: This needs to be adjusted with the right panel menu overhaul
            self.refresh_active_menu("hex")
