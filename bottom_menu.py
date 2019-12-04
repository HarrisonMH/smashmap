# bottom_menu.py
#
# Define properties of bottom menu


import tkinter as tk
from player_status_bar import PlayerStatusBar


class BottomMenu(tk.Frame):

    def __init__(self, master, player_list, player_menu_callback, end_turn_callback, icon_image_dict):
        super().__init__(master)
        self._master = master
        self._player_menu_callback = player_menu_callback
        self._end_turn_callback = end_turn_callback
        self._icon_image_dict = icon_image_dict
        self._player_list = player_list
        self._player_button_list = []
        self._player_status_bar_list = []
        self._create_widgets(self._player_list)

    def _create_widgets(self, player_list):
        # current_col = 0
        # for player in self._player_list:
        #     player_label = "Player " + str(player.get_player_number()) + ": " + player.get_name()
        #     self._player_button_list.append(tk.Label(self, width=11, text=player_label, font=(None, 14), fg="white",
        #                                              bg=player.get_colour(), borderwidth=4, relief="groove"))
        #     self._player_button_list[-1].grid(row=0, column=current_col, padx=(10))
        #     # self._player_button_list[-1].bind("<Button-1>", self._player_menu_callback)
        #     self._player_button_list[-1].bind("<Button-1>", player.show_player_menu)
        #     current_col += 1

        current_col = 0
        for player in player_list:
            self._player_status_bar_list.append(PlayerStatusBar(self, player, self._icon_image_dict))
            self._player_status_bar_list[-1].grid(row=0, column=current_col)
            current_col += 1

        # self._end_button = tk.Button(self, text="Refresh All", command=self._end_turn_callback)
        # self._end_button.grid(row=0, column=current_col)
        # current_col += 1

    def refresh_widget_order(self, player_list):
        new_widget_list = []
        for status_bar in self._player_status_bar_list:
            status_bar.grid_forget()
        current_col = 0
        for player in player_list:
            for status_bar in self._player_status_bar_list:
                if player == status_bar.get_owner():
                    new_widget_list.append(status_bar)
                    new_widget_list[-1].grid(row=0, column=current_col)
                    current_col += 1
        self._player_status_bar_list = new_widget_list


