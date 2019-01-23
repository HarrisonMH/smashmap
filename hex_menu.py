# hex_menu.py

import tkinter as tk
import copy


class HexMenu(tk.Frame):

    def __init__(self, master, hex):
        # super().__init__()
        tk.Frame.__init__(self, master)
        self._master = master
        self._hex = hex
        # self._hex_id = self._hex.get_id()

        self._create_widgets()


    def _create_widgets(self):
        current_row = 0
        self._header = tk.Label(self, width=30, text="Hex " + str(self._hex.get_id()), font=(None, 16))
        self._header.grid(row=current_row, column=0, pady=(1, 10))
        current_row += 1
        self._owner_label = tk.Label(self, text="Owner: " + self._hex.get_owner(), font=(None, 10))
        self._owner_label.grid(row=current_row, column=0)
        current_row += 1
        self._strucures_header = tk.Label(self, text="Structure Present: " + self._hex.get_structure())
        self._strucures_header.grid(row=current_row, column=0)
        current_row += 1
        self._adjacency_label = tk.Label(self, text="Hex Coordinates: " + str(self._hex.get_coords()))
        self._adjacency_label.grid(row=current_row, column=0)
        current_row += 1
        self._adjacency_label = tk.Label(self, text="Adjacent Hexes: " + self.get_adjacency_str())
        self._adjacency_label.grid(row=current_row, column=0)
        current_row += 1
        self._squads_header = tk.Label(self, text="Squads Present", font=(None, 14))
        self._squads_header.grid(row=current_row, column=0, columnspan=5)


        print(self._hex.get_squads())



        # squads = self._hex.get_squads()
        # if squads[0] is not None:
        #     self._squad_1_label = copy.deepcopy(squads[0])
        #     self._squad_1_label.grid(row=current_row, column=0, columnspan=2)
        # if squads[1] is not None:
        #     self._squad_2_label = copy.deepcopy(squads[1])
        #     self._squad_2_label.grid(row=current_row, column=3, columnspan=2)


    def get_adjacency_str(self):
        adj_list = self._hex.get_adjacent_ids()
        list_len = len(adj_list)
        adj_string = ""
        for i, hex in enumerate(adj_list):
            adj_string += str(hex)
            if i < list_len - 1:
                adj_string += ", "
        return adj_string
