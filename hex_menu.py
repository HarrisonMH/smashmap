# hex_menu.py

import tkinter as tk
import tkinter.ttk as ttk
from squad_menu_icon import SquadMenuIcon
from squad_menu import SquadMenu


class HexMenu(tk.Frame):

    def __init__(self, hex, hex_map, fighter_image_dict, fighter_list):
        # super().__init__()
        tk.Frame.__init__(self)
        self._menu_name = "hex"
        self._master = None
        self._hex = hex
        self._hex_map = hex_map
        self._fighter_image_dict = fighter_image_dict
        self._fighter_list = fighter_list
        self._squad_icon_list = []

        self._hex_owner = self._hex.get_owner()
        if self._hex_owner is not None:
            self._player_str = "Player " + str(self._hex_owner.get_player_number())
            self._player_colour = self._hex_owner.get_colour()
        else:
            self._player_str = "Unclaimed Hex"
            self._player_colour = "white"

        self._create_widgets()


    def _create_widgets(self):
        self._current_row = 0
        if self._hex_owner is not None:
            self._player_num_header = tk.Label(self, width=30, text=self._player_str,
                                               font=(None, 16))
            self._player_num_header.grid(row=0, column=0, columnspan=5)
            self._current_row += 1
        self._player_name_header = tk.Label(self, text=self._hex.get_owner_name_str(), width=10, font=(None, 16),
                                            bg=self._player_colour, borderwidth=2, relief="solid")
        self._player_name_header.grid(row=self._current_row, column=0, columnspan=5, pady=(1, 10))
        self._current_row += 1
        self._header = tk.Label(self, width=30, text="Hex " + str(self._hex.get_id()), font=(None, 16))
        self._header.grid(row=self._current_row, column=0, columnspan=2, pady=(1, 10))
        self._current_row += 1
        # self._owner_label = tk.Label(self, text="Owner: " + self._hex.get_owner_name_str(), font=(None, 10))
        # self._owner_label.grid(row=self._current_row, column=0, columnspan=2)
        # self._current_row += 1
        # self._structures_header = tk.Label(self, text="Structure Present: " + self._hex.get_structure())
        # self._structures_header.grid(row=self._current_row, column=0, columnspan=2)
        # self._current_row += 1
        self._coordinate_label = tk.Label(self, text="Hex Coordinates: " + str(self._hex.get_coords()))
        self._coordinate_label.grid(row=self._current_row, column=0, columnspan=2)
        self._current_row += 1
        self._adjacency_label = tk.Label(self, text="Adjacent Hexes: " + self.get_adjacency_str())
        self._adjacency_label.grid(row=self._current_row, column=0, columnspan=2)
        self._current_row += 1
        # self._ring_label = tk.Label(self, text="Ring Depth: " + str(self._hex.get_ring_depth()))
        # self._ring_label.grid(row=self._current_row, column=0, columnspan=2)
        # self._current_row += 1
        self._res_value_label = tk.Label(self, text="Resource Value: " + str(self._hex.get_value()), font=(None, 10))
        self._res_value_label.grid(row=self._current_row, column=0, columnspan=2)
        self._current_row += 1
        self._vp_value_label = tk.Label(self, text="VP Value: " + str(self._hex.get_vp_value()), font=(None, 10))
        self._vp_value_label.grid(row=self._current_row, column=0, columnspan=2)
        self._current_row += 1

        structure = self._hex.get_structure()
        if structure != "None":
            if structure == "Mine":
                structure_str = "Mine (+25 Res. +1 VP)"
            elif structure == "Factory":
                structure_str = "Factory (Build)"
            elif structure == "Refinery":
                structure_str = "Refinery (+175 Res, +5 VP)"
            elif structure == "HQ":
                structure_str = "HQ (+175 Res, Build)"
            self._structure_header = tk.Label(self, text="Structure: " + structure_str, font=(None, 14))
            self._structure_header.grid(row=self._current_row, column=0, columnspan=2, pady=(1, 10))
            self._current_row += 1
            if structure == "HQ" or structure == "Factory":
                self._build_squad_label = tk.Label(self, text="New squad: ")
                self._build_squad_label.grid(row=self._current_row, column=0, columnspan=1, pady=10)
                self._build_squad_picker = ttk.Combobox(self, values=self._fighter_list)
                self._build_squad_picker.grid(row=self._current_row, column=1, columnspan=1, pady=10)
                self._current_row += 1
                self._build_squad_btn = tk.Button(self, text="Build", font=(None, 10, "bold"), command=self._build_new_squad)
                self._build_squad_btn.grid(row=self._current_row, column=0, columnspan=1, pady=10)
                self._current_row += 1

        # Placeholder for squad menu
        self._squad_menu = tk.Frame()

        if self._hex.check_if_squad_present():
            self._squads_header = tk.Label(self, text="Squads Present", font=(None, 14))
            self._squads_header.grid(row=self._current_row, column=0, columnspan=2, pady=10)
            self._current_row += 1
            current_col = 0
            for squad in self._hex.get_squads():
                # print(squad)
                if squad is not None:
                    fighter_name = squad.get_fighter()
                    self._squad_icon_list.append(SquadMenuIcon(self, squad, self._squad_menu_callback,
                                                               self._fighter_image_dict[fighter_name]["menu"]))
                    self._squad_icon_list[-1].grid(row=self._current_row, column=current_col, pady=(5, 10))
                    current_col += 1
            self._current_row += 1



        # print(self._hex.get_squads())



        # squads = self._hex.get_squads()
        # if squads[0] is not None:
        #     self._squad_1_label = copy.deepcopy(squads[0])
        #     self._squad_1_label.grid(row=self.current_row, column=0, columnspan=2)
        # if squads[1] is not None:
        #     self._squad_2_label = copy.deepcopy(squads[1])
        #     self._squad_2_label.grid(row=self.current_row, column=3, columnspan=2)


    def get_adjacency_str(self):
        adj_list = self._hex.get_adjacent_ids()
        list_len = len(adj_list)
        adj_string = ""
        for i, hex in enumerate(adj_list):
            adj_string += str(hex)
            if i < list_len - 1:
                adj_string += ", "
        return adj_string

    def _build_new_squad(self):
        fighter = self._build_squad_picker.get()
        if fighter != "":
            self._hex.get_owner().build_squad(fighter, self._hex)

    def _squad_menu_callback(self, squad, event):
        self._squad_menu.grid_forget()
        self._squad_menu = SquadMenu(self, squad, self._hex_map, self._menu_name)
        self._squad_menu.grid(row=self._current_row, column=0, columnspan=2)
        for icon in self._squad_icon_list:
            icon.set_relief("groove")
        event.widget.config(relief="sunken")