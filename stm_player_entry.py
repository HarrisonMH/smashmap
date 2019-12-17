# stm_player_entry
#
# Tkinter compound widget for player input at the start menu

import tkinter as tk
import tkinter.ttk as ttk
from colour_picker import ColourPicker


class PlayerEntry(tk.Frame):
    def __init__(self, master, player_num, fighter_list, **kwargs):
        super().__init__(master, kwargs)

        self._start_menu_ref = master
        self._player_num = player_num
        self._fighter_list = fighter_list
        self._random_check_var = tk.IntVar()

        self._create_widgets()

    def _create_widgets(self):
        current_row = 0

        # Headers
        self._player_label = tk.Label(self, text="Player " + str(self._player_num) + ":", font=(None, 12))
        self._player_label.grid(row=current_row, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        self._handicap_label = tk.Label(self, text="Handicap Options:", anchor="w", font=(None, 8, "bold"))
        self._handicap_label.grid(row=current_row, column=4, columnspan=1, sticky="w")
        current_row += 1

        # Name and Colour entry
        self._name_label = tk.Label(self, text="Name: ")
        self._name_label.grid(row=current_row, column=0, padx=10, pady=5, sticky="w")
        self._name_entry = tk.Entry(self)
        self._name_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="w")
        self._colour_label = tk.Label(self, text="Colour: ")
        self._colour_label.grid(row=current_row, column=2, padx=10, pady=5, sticky="w")
        self._colour_entry = ColourPicker(self, self._start_menu_ref, self._player_num)
        self._colour_entry.grid(row=current_row, column=3, padx=10, pady=5, sticky="w" + "e")

        # Handicap Options Box
        self._handicap_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self._handicap_frame.grid(row=current_row, column=4, rowspan=2)
        self._cost_handicap_label = tk.Label(self._handicap_frame, text="Base Squad Cost:")
        self._cost_handicap_label.grid(row=0, column=0)
        self._cost_handicap_scale = tk.Scale(self._handicap_frame, from_=250, to=500, resolution=25, orient="horizontal")
        self._cost_handicap_scale.grid(row=0, column=1)
        self._random_handicap_label = tk.Label(self._handicap_frame, text="All Random Squads:")
        self._random_handicap_label.grid(row=1, column=0)
        self._random_handicap_checkbox = tk.Checkbutton(self._handicap_frame, variable=self._random_check_var, command=self.toggle_random_squads)
        self._random_handicap_checkbox.grid(row=1, column=1)
        current_row += 1

        # Squad entry
        self._squad_1_label = tk.Label(self, text="Squad 1: ")
        self._squad_1_label.grid(row=current_row, column=0, padx=10, pady=5, sticky="w")
        self._squad_1_picker = ttk.Combobox(self, values=self._fighter_list, state="readonly")
        self._squad_1_picker.grid(row=current_row, column=1, padx=10, pady=5, sticky="w")

        self._squad_2_label = tk.Label(self, text="Squad 2: ")
        self._squad_2_label.grid(row=current_row, column=2, padx=10, pady=5, sticky="w")
        self._squad_2_picker = ttk.Combobox(self, values=self._fighter_list, state="readonly")
        self._squad_2_picker.grid(row=current_row, column=3, padx=10, pady=5, sticky="w")


    def get_name(self):
        return self._name_entry.get()

    def get_colour(self):
        return self._colour_entry.get_colour()

    def get_fighter_1(self):
        return self._squad_1_picker.get()

    def get_fighter_2(self):
        return self._squad_2_picker.get()

    def get_base_cost(self):
        return self._cost_handicap_scale.get()

    def get_force_random(self):
        return self._random_check_var.get()

    def toggle_random_squads(self):
        if self._random_check_var.get() == 1:
            self._squad_1_picker.set("Random")
            self._squad_2_picker.set("Random")
            self._squad_1_picker.config(state="disabled")
            self._squad_2_picker.config(state="disabled")
        elif self._random_check_var.get() == 0:
            self._squad_1_picker.config(state="readonly")
            self._squad_2_picker.config(state="readonly")
