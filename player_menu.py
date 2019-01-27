# player_menu.py
#
# Defines attributes for Player Details side menu

import tkinter as tk
from squad_menu import SquadMenu
from squad_menu_icon import SquadMenuIcon

class PlayerMenu(tk.Frame):

    def __init__(self, master, player, fighter_image_dict, hex_map):
        super().__init__(master)
        self._master = master
        self._player = player
        self._fighter_image_dict = fighter_image_dict
        self._hex_map = hex_map
        self._squad_icon_list = []
        self._create_widgets()


    def _create_widgets(self):
        # Placeholder variable, not rendered
        self._squad_menu = tk.Frame()

        current_row = 0
        self._header_1 = tk.Label(self, width=30, text="Player " + str(self._player.get_player_number()), font=(None, 16))
        self._header_1.grid(row=0, column=0, columnspan=5)
        current_row +=1
        self._header_2 = tk.Label(self, text=self._player.get_name(), width=10, font=(None, 16), bg=self._player.get_colour(), borderwidth=2, relief="solid")
        self._header_2.grid(row=current_row, column=0, columnspan=5, pady=(1, 10))
        current_row += 1
        self._resources = tk.Label(self, text="Resources: " + str(self._player.get_resources()), font=(None, 13), justify="left", anchor="w", borderwidth=2)
        self._resources.grid(row=current_row, column=0)

        self._income = tk.Label(self, text="Income: " + str(self._player.get_income()), font=(None, 13), justify="left", anchor="w")
        self._income.grid(row=current_row, column=2)
        current_row += 1
        self._territory = tk.Label(self, text="Territory Controlled: " + str(self._player.get_territory_size()), font=(None, 13), justify="left", anchor="w")
        self._territory.grid(row=current_row, column=0)

        self._hq_label = tk.Label(self, text="HQ: Hex " + str(self._player.get_hq().get_id()), font=(None, 13))
        self._hq_label.grid(row=current_row, column=2)
        current_row += 1
        self._squads_header = tk.Label(self, text="Squads: ", font=(None, 13, "bold"))
        self._squads_header.grid(row=current_row, column=0, columnspan=5)

        current_row += 1
        current_col = 0
        for squad in self._player.get_squads():
            fighter_name = squad.get_fighter()
            self._squad_icon_list.append(SquadMenuIcon(self, squad, self._squad_menu_callback, self._fighter_image_dict[fighter_name]["menu"]))
            self._squad_icon_list[-1].grid(row=current_row, column=current_col, pady=(5, 10))
            if current_col >= 5:
                current_col = 0
                current_row += 1
            else:
                current_col += 1


    def _squad_menu_callback(self, squad, event):
        self._squad_menu.grid_forget()
        self._squad_menu = SquadMenu(self, squad, self._hex_map)
        self._squad_menu.grid(row=10, column=0, columnspan=5)
        for icon in self._squad_icon_list:
            icon.set_relief("groove")
        event.widget.config(relief="sunken")
