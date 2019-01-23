# bottom_menu.py
#
# Define properties of bottom menu


import tkinter as tk


class BottomMenu(tk.Frame):

    def __init__(self, master, player_data, player_menu_callback):
        super().__init__(master)
        self._master = master
        self._player_menu_callback = player_menu_callback
        self._player_data = player_data
        self._player_list = []
        self._create_widgets()

    def _create_widgets(self):
        num_players = len(self._player_data)
        current_col = 0
        for i in range(num_players):
            player_str = "p" + str(i + 1)
            player_label = "Player " + str(i + 1) + ": " + self._player_data[player_str]["name"]
            self._player_list.append(tk.Label(self, width=11, text=player_label, font=(None, 14), fg="white", bg=self._player_data[player_str]["colour"], borderwidth=4, relief="groove"))
            self._player_list[-1].grid(row=0, column=current_col, padx=(10))
            self._player_list[-1].bind("<Button-1>", self._player_menu_callback)
            current_col += 1

