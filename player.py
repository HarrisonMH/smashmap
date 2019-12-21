# player.py
#
# Defines and stores player attributes

import tkinter as tk

from squad import Squad
import random as r


class Player:

    def __init__(self, master, player_data, hex_map_ref, create_squad_icon_callback, hex_menu_callback,
                 battle_popup_callback, get_current_player_callback, is_load=False):
        self._master = master
        self._hex_map_ref = hex_map_ref
        self._create_squad_icon_callback = create_squad_icon_callback
        self._hex_menu_callback = hex_menu_callback
        self._battle_popup_callback = battle_popup_callback
        self._get_current_player_callback = get_current_player_callback
        self._play_log_ref = master.get_play_log()
        self._player_number = int(player_data["playernum"])
        self._name = player_data["name"]
        self._colour = player_data["colour"]
        if is_load is False:
            self._starting_squads = [player_data["fighter1"], player_data["fighter2"]]
        else:
            self._starting_squads = None
        self._hq = None
        self._resources = 750
        self._income = 250
        self._base_squad_cost = player_data["basecost"]
        self._force_random_squad_selection = player_data["forcerandom"]
        self._territory_size = 4
        self._vp = 0
        self._vp_income = 7
        self._squads = []
        self._status_bar_ref = None


    def get_player_number(self):
        return self._player_number

    def get_name(self):
        return self._name

    def get_colour(self):
        return self._colour

    def get_resources(self):
        return self._resources

    def set_resources(self, amount):
        self._resources = amount

    def adjust_resources(self, amount):
        self._resources += amount
        if self._status_bar_ref is not None:
            self._status_bar_ref.set_res(self._resources)

    def get_income(self):
        return self._income

    def set_income(self, amount):
        self._income = amount

    def adjust_income(self, amount):
        self._income += amount
        self._status_bar_ref.set_res_income(self._income)

    def collect_income(self):
        self._resources += self._income
        self._status_bar_ref.set_res(self._resources)

    def get_territory_size(self):
        return self._territory_size

    def set_territory_size(self, value):
        self._territory_size = value

    def adjust_territory_size(self, increment):
        self._territory_size += increment
        self._status_bar_ref.set_territory_size(self._territory_size)

    def get_vp(self):
        return self._vp

    def set_vp(self, value):
        self._vp = value

    def adjust_vp(self, amount):
        self._vp += amount
        self._status_bar_ref.set_vp(self._vp)

    def collect_vp(self):
        self._vp += self._vp_income
        self._status_bar_ref.set_vp(self._vp)

    def get_vp_income(self):
        return self._vp_income

    def set_vp_income(self, value):
        self._vp_income = value

    def adjust_vp_income(self, amount):
        self._vp_income += amount
        self._status_bar_ref.set_vp_income(self._vp_income)

    def get_squads(self, debug=False):
        if debug is True:
            i = 1
            print("Player squads:")
            for squad in self._squads:
                print("Squad ", i, ": ", squad.get_fighter(), " in Hex ", squad.get_location().get_id())
                i += 1
        return self._squads

    def get_idle_squads(self):
        idle_squad_list = []
        for squad in self._squads:
            if squad.get_turn_status() is False:
                idle_squad_list.append(squad)
        return idle_squad_list

    def refresh_player_squads(self):
        for squad in self.get_squads():
            squad.refresh_turn()

    def get_hq(self):
        return self._hq

    def set_hq(self, new_hq):
        self._hq = new_hq
        if self._starting_squads is not None:
            if self._starting_squads[0] == self._starting_squads[1] and self._starting_squads[0] != "Random":
                self.adjust_resources(-250)
            self._initialize_squads(self._starting_squads)

    def set_status_bar_ref(self, ref):
        self._status_bar_ref = ref

    # def build_squad(self, fighter, hex_id):
    #     # self._squads.append(Squad(self._name, fighter, hex_id, self._place_squad_icon_callback))
    #     self._squads.append(Squad(self, fighter, hex_id, self._place_squad_icon_callback))

    def get_base_squad_cost(self):
        return self._base_squad_cost

    def set_base_squad_cost(self, value):
        self._base_squad_cost = value

    def build_squad(self, fighter, hex, active_menu=None):
        new_fighter = fighter
        squad_cost = self.get_new_squad_cost(new_fighter)
        if new_fighter == "Random":
            fighter_list = self._master.get_fighter_list()
            new_fighter = fighter_list[r.randint(1, len(fighter_list) - 1)]
        if self._resources - squad_cost < 0:
            print("Player resources insufficient to build squad")
            return
        elif hex.check_open_space() is False:
            print("Cannot build, hex is full")
        else:
            self._squads.append(Squad(self, new_fighter, hex, self._create_squad_icon_callback, self._battle_popup_callback,
                                      self._master.set_selected_squad, self._master.get_selected_squad,
                                      self._get_current_player_callback))
            self.adjust_resources(squad_cost * -1)
            if hex.get_structure() == "Factory":
                self._squads[-1].take_turn()
            if active_menu is not None:
                self._squads[-1].refresh_active_menu(active_menu)
            # print("Building squad in hex: ", hex)
        self._master.next_player()

    def load_squad(self, squad_dict):
        hex_list = self._hex_map_ref.get_hex_list()
        fighter = squad_dict["fighter"]
        hex_location = hex_list[int(squad_dict["location"]) - 1]
        self._squads.append(Squad(self, fighter, hex_location, self._create_squad_icon_callback, self._battle_popup_callback,
                                  self._master.set_selected_squad, self._master.get_selected_squad,
                                  self._get_current_player_callback))
        self._squads[-1].increment_kills(squad_dict["kills"])
        if squad_dict["turn_taken"] is True:
            self._squads[-1].take_turn()

    def destroy_squad(self, squad):
        print("Deleting Squad object: ", squad)
        self._squads.remove(squad)

    def check_remaining_actions(self):
        for squad in self._squads:
            if squad.get_turn_status() is False:
                return True
        if self._resources >= self._base_squad_cost:
            return True
        return False

    # def show_player_menu(self, event=None):
    #     self._player_menu_callback(self)

    def _initialize_squads(self, starting_squads):
        self.build_squad(starting_squads[0], self._hq)
        self.build_squad(starting_squads[1], self._hq)

    def get_new_squad_cost(self, fighter):
        """Charity rule: Allow player to build a new squad for all of their resources if they have no other squads and
        cannot afford the full cost"""
        base_cost = self._base_squad_cost
        multiplier = 1
        if len(self._squads) == 0:
            if self._resources <= base_cost:
                return self._resources
            else:
                return base_cost
        else:
            for squad in self._squads:
                if squad.get_fighter() == fighter:
                    multiplier += 1
            return base_cost * multiplier

    def get_force_random(self):
        return self._force_random_squad_selection

    def set_force_random(self, value):
        self._force_random_squad_selection = value

    def get_main_window(self):
        return self._master
