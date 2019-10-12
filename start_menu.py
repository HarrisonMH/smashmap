#start_menu.py

import tkinter as tk
import tkinter.ttk as ttk

NAME_ENTRY = 2
COLOUR_ENTRY = 4
FIGHTER_1_ENTRY = 6
FIGHTER_2_ENTRY = 8

class StartMenu(tk.Frame):


    def __init__(self, master, fighter_list, start_game_callback):
        tk.Frame.__init__(self, master)
        self._master = master
        self._fighter_list = fighter_list
        self._start_game_callback = start_game_callback
        self._players = []

        self._create_widgets()


    def _create_widgets(self):
        self._header = tk.Label(self, text="Enter Player Data", font=(None, 16))
        self._header.grid(row=0, column=0, columnspan=4)
        self._create_player_fields()


    def _create_player_fields(self):
        player_num = 1
        for player in range(6):
            # Creates widgets for each player.
            player_var = tk.StringVar()
            player_var.set("player" + str(player_num))

            self._players.append([])
            self._players[player].append(tk.Label(self, text="Player " + str(player_num) + ":", font=(None, 12)))
            self._players[player].append(tk.Label(self, text="Name: "))
            self._players[player].append(tk.Entry(self))
            #FIXME: Change colour input to Combobox
            self._players[player].append(tk.Label(self, text="Colour: "))
            self._players[player].append(tk.Entry(self))
            self._players[player].append(tk.Label(self, text="Squad 1: "))
            self._players[player].append(ttk.Combobox(self, values=self._fighter_list))
            self._players[player].append(tk.Label(self, text="Squad 2: "))
            self._players[player].append(ttk.Combobox(self, values=self._fighter_list))

            player_num += 1

        current_row = 2
        for player_data in self._players:
            current_col = 0

            player_data[0].grid(row=current_row, column=current_col, pady=(8, 1))
            current_row += 1

            for i in range(1, 5):
                player_data[i].grid(row=current_row, column=current_col)
                current_col +=1

            current_row += 1
            current_col = 0

            for i in range(5, 9):
                player_data[i].grid(row=current_row, column=current_col, pady=(8, 1))
                current_col += 1
                if i == 8:
                    player_data[i].grid(padx=(1, 5))

            current_row += 1

        self._start_button = tk.Button(self, text="Start!", font=(None, 20),  command=self.start_game)
        self._start_button.grid(row=current_row, column=0, columnspan=4, pady=20)

        current_row += 1
        self._start_test = tk.Button(self, text="Start With Test Data", font=(None, 12), command=self.start_test)
        self._start_test.grid(row=current_row, column=0, columnspan=4, pady=20)


    def start_game(self):
        player_data = {}
        current_player = 1
        for _player_inputs in self._players:
            player_key = "p" + str(current_player)
            if _player_inputs[NAME_ENTRY].get() == "":
                continue
            player_data[player_key] = {}
            player_data[player_key]["playernum"] = current_player
            player_data[player_key]["name"] = _player_inputs[NAME_ENTRY].get()
            player_data[player_key]["colour"] = _player_inputs[COLOUR_ENTRY].get()
            player_data[player_key]["fighter1"] = _player_inputs[FIGHTER_1_ENTRY].get()
            player_data[player_key]["fighter2"] = _player_inputs[FIGHTER_2_ENTRY].get()
            current_player += 1

        self._start_game_callback(player_data)


    def start_test(self):
        test_player_data = {'p1': {'playernum': 1, 'name': 'Matt', 'colour': 'goldenrod', 'fighter1': 'Peach',
                                   'fighter2': 'Captain Falcon'},
                            'p2': {'playernum': 2, 'name': 'Joe', 'colour': 'red', 'fighter1': 'Ness',
                                   'fighter2': 'Joker'},
                            'p3': {'playernum': 3, 'name': 'Alex', 'colour': 'green', 'fighter1': 'Ganondorf',
                                   'fighter2': 'Villager'},
                            'p4': {'playernum': 4, 'name': 'Kit', 'colour': 'darkorange', 'fighter1': 'Ness',
                                   'fighter2': 'Zelda'},
                            'p5': {'playernum': 5, 'name': 'Alvin', 'colour': 'royalblue', 'fighter1': 'Cloud',
                                   'fighter2': 'Ryu'},
                            'p6': {'playernum': 6, 'name': 'Eric', 'colour': 'purple', 'fighter1': 'Inkling',
                                   'fighter2': 'Pikachu'}}
        self._start_game_callback(test_player_data)




