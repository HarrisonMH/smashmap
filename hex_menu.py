# hex_menu.py

import tkinter as tk
from squad_menu_icon import SquadMenuIcon
from squad_menu import SquadMenu


class HexMenu(tk.Frame):

    def __init__(self, hex, hex_map, fighter_image_dict):
        # super().__init__()
        tk.Frame.__init__(self)
        self._menu_name = "hex"
        self._master = None
        self._hex = hex
        self._hex_map = hex_map
        self._fighter_image_dict = fighter_image_dict
        self._squad_icon_list = []

        self._create_widgets()


    def _create_widgets(self):
        self._current_row = 0
        self._header = tk.Label(self, width=30, text="Hex " + str(self._hex.get_id()), font=(None, 16))
        self._header.grid(row=self._current_row, column=0, columnspan=2, pady=(1, 10))
        self._current_row += 1
        self._owner_label = tk.Label(self, text="Owner: " + self._hex.get_owner(), font=(None, 10))
        self._owner_label.grid(row=self._current_row, column=0, columnspan=2)
        self._current_row += 1
        self._strucures_header = tk.Label(self, text="Structure Present: " + self._hex.get_structure())
        self._strucures_header.grid(row=self._current_row, column=0, columnspan=2)
        self._current_row += 1
        self._adjacency_label = tk.Label(self, text="Hex Coordinates: " + str(self._hex.get_coords()))
        self._adjacency_label.grid(row=self._current_row, column=0, columnspan=2)
        self._current_row += 1
        self._adjacency_label = tk.Label(self, text="Adjacent Hexes: " + self.get_adjacency_str())
        self._adjacency_label.grid(row=self._current_row, column=0, columnspan=2)
        self._current_row += 1

        # Placeholder for squad menu
        self._squad_menu = tk.Frame()

        if self._hex.check_if_squad_present():
            self._squads_header = tk.Label(self, text="Squads Present", font=(None, 14))
            self._squads_header.grid(row=self._current_row, column=0, columnspan=2, pady=10)
            self._current_row += 1
            current_col = 0
            for squad in self._hex.get_squads():
                if squad is not None:
                    fighter_name = squad.get_fighter()
                    self._squad_icon_list.append(SquadMenuIcon(self, squad, self._squad_menu_callback,
                                                               self._fighter_image_dict[fighter_name]["menu"]))
                    self._squad_icon_list[-1].grid(row=self._current_row, column=current_col, pady=(5, 10))
                    current_col += 1
            self._current_row += 1


        print(self._hex.get_squads())



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


    def _squad_menu_callback(self, squad, event):
        self._squad_menu.grid_forget()
        self._squad_menu = SquadMenu(self, squad, self._hex_map, self._menu_name)
        self._squad_menu.grid(row=self._current_row, column=0, columnspan=2)
        for icon in self._squad_icon_list:
            icon.set_relief("groove")
        event.widget.config(relief="sunken")