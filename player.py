# player.py
#
# Defines and stores player attributes

import tkinter as tk

from squad import Squad

class Player():

    def __init__(self, master, player_data, place_squad_icon_callback, player_menu_callback, hex_menu_callback, battle_popup_callback):
        self._master = master
        self._place_squad_icon_callback = place_squad_icon_callback
        self._player_menu_callback = player_menu_callback
        self._hex_menu_callback = hex_menu_callback
        self._battle_popup_callback = battle_popup_callback
        self._player_number = player_data["playernum"]
        self._name = player_data["name"]
        self._colour = player_data["colour"]
        self._starting_squads = [player_data["fighter1"], player_data["fighter2"]]
        self._hq = None
        self._resources = 250
        self._income = 100
        self._territory_size = 4
        self._squads = []


    def get_player_number(self):
        return self._player_number

    def get_name(self):
        return self._name

    def get_colour(self):
        return self._colour

    def get_resources(self):
        return self._resources

    def adjust_resources(self, amount):
        self._resources += amount

    def get_income(self):
        return self._income

    def set_income(self, income):
        self._income = income

    def get_territory_size(self):
        return self._territory_size

    def adjust_territory_size(self, increment):
        self._territory_size += increment

    def get_squads(self):
        return self._squads

    def get_hq(self):
        return self._hq

    def set_hq(self, new_hq):
        self._hq = new_hq
        if self._starting_squads[0] == self._starting_squads[1]:
            self.adjust_resources(-250)
        self._initialize_squads(self._starting_squads)

    # def build_squad(self, fighter, hex_id):
    #     # self._squads.append(Squad(self._name, fighter, hex_id, self._place_squad_icon_callback))
    #     self._squads.append(Squad(self, fighter, hex_id, self._place_squad_icon_callback))

    def build_squad(self, fighter, hex):
        # self._squads.append(Squad(self._name, fighter, hex_id, self._place_squad_icon_callback))
        self._squads.append(Squad(self, fighter, hex, self._place_squad_icon_callback, self._battle_popup_callback))

    def show_player_menu(self, event=None):
        self._player_menu_callback(self)

    def _initialize_squads(self, starting_squads):
        self.build_squad(starting_squads[0], self._hq)
        self.build_squad(starting_squads[1], self._hq)
