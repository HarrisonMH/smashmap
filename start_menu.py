#start_menu.py

import tkinter as tk
import tkinter.ttk as ttk
from colour_picker import ColourPicker
from stm_player_entry import PlayerEntry

NAME_ENTRY = 2
COLOUR_ENTRY = 4
FIGHTER_1_ENTRY = 6
FIGHTER_2_ENTRY = 8


class StartMenu(tk.Frame):

    def __init__(self, master, fighter_list, start_game_callback, load_game_callback):
        tk.Frame.__init__(self, master)
        self._master = master
        self._fighter_list = fighter_list
        self._start_game_callback = start_game_callback
        self._load_game_callback = load_game_callback
        self._selected_colour_list = []
        self._players = []

        self._random_check_var = tk.IntVar()

        self._create_widgets()


    def _create_widgets(self):
        self._header = tk.Label(self, text="Enter Player Data", font=(None, 16))
        self._header.grid(row=0, column=0, columnspan=4, sticky="w")
        self._create_player_fields()


    def _create_player_fields(self):
        player_num = 1
        current_row = 1
        input_width = 8
        for player in range(6):
            # Creates widgets for each player.
            self._players.append(PlayerEntry(self, player, self._fighter_list))
            self._players[-1].grid(row=current_row, column=0)
            current_row += 1
            player_num += 1

        self._start_button = tk.Button(self, text="Start!", font=(None, 20),  command=self.start_game)
        self._start_button.grid(row=current_row, column=0, columnspan=5, pady=20)

        current_row += 1
        self._start_test = tk.Button(self, text="Start With Test Data", font=(None, 12), command=self.start_test)
        self._start_test.grid(row=current_row, column=0)
        self._load_game_btn = tk.Button(self, text="Load Game", font=(None, 12), command=self.load_game)
        self._load_game_btn.grid(row=current_row, column=1)

    def change_selected_colours(self, new_value, old_value=None):
        if old_value is not None:
            self._selected_colour_list.remove(old_value)
        self._selected_colour_list.append(new_value)

    def get_selected_colour_list(self):
        return self._selected_colour_list

    def start_game(self):
        player_data = {}
        current_player = 1
        for _player_inputs in self._players:
            player_key = "p" + str(current_player)
            if _player_inputs[NAME_ENTRY].get() == "":
                continue
            player_data[player_key] = {}
            player_data[player_key]["playernum"] = current_player
            player_data[player_key]["name"] = _player_inputs.get_name()
            player_data[player_key]["colour"] = _player_inputs.get_colour()
            player_data[player_key]["fighter1"] = _player_inputs.get_fighter_1()
            player_data[player_key]["fighter2"] = _player_inputs.get_fighter_2()
            player_data[player_key]["basecost"] = _player_inputs.get_base_cost()
            player_data[player_key]["forcerandom"] = _player_inputs.get_force_random()
            current_player += 1

        self._start_game_callback(player_data)

    def load_game(self):
        self._load_game_callback()

    def start_test(self):
        test_player_data = {'p1': {'playernum': 1, 'name': 'Matt', 'colour': 'goldenrod', 'fighter1': 'Peach',
                                   'fighter2': 'Captain Falcon', 'basecost': 300, 'forcerandom': 1},
                            'p2': {'playernum': 2, 'name': 'Joe', 'colour': 'red', 'fighter1': 'Ness',
                                   'fighter2': 'Joker', 'basecost': 250, 'forcerandom': 1},
                            'p3': {'playernum': 3, 'name': 'Alex', 'colour': 'green', 'fighter1': 'Ganondorf',
                                   'fighter2': 'Villager', 'basecost': 250, 'forcerandom': 1},
                            'p4': {'playernum': 4, 'name': 'Kit', 'colour': 'darkorange', 'fighter1': 'Ness',
                                   'fighter2': 'Zelda', 'basecost': 250, 'forcerandom': 1},
                            'p5': {'playernum': 5, 'name': 'Alvin', 'colour': 'darkcyan', 'fighter1': 'Cloud',
                                   'fighter2': 'Ryu', 'basecost': 250, 'forcerandom': 1},
                            'p6': {'playernum': 6, 'name': 'Eric', 'colour': 'indigo', 'fighter1': 'Inkling',
                                   'fighter2': 'Pikachu', 'basecost': 250, 'forcerandom': 1}}
        self._start_game_callback(test_player_data)




