# end_turn_popup.py
#
# Defines attributes, methods, and layout for the dialog popup that occurs when attempting to end turn while players
# have actions remaining

import tkinter as tk


class EndTurnPopup(tk.Toplevel):

    def __init__(self, master, player_list, close_window_callback, refresh_actions_callback):
        super().__init__(master, borderwidth=4, relief="raised")
        self._player_list = player_list
        self._player_label_list = []

        self._close_window_callback = close_window_callback
        self._confirm_btn_callback = refresh_actions_callback

        self.title = "Confirm"
        self.resizable(False, False)
        self.geometry("+400+300")
        self.overrideredirect(True)

        self._create_widgets()

    def _create_widgets(self):
        current_row = 0
        self._warning = tk.Label(self, text="The following players still have actions remaining:", font=(None, 10, "bold"))
        self._warning.grid(row=current_row, column=0, columnspan=2)
        current_row += 1
        for player in self._player_list:
            self._player_label_list.append(tk.Label(self, width=11, text=player.get_name(), font=(None, 14), fg="white",
                                                    bg=player.get_colour(), borderwidth=4, relief="raised"))
            self._player_label_list[-1].grid(row=current_row, column=0)
            current_row += 1
        self._confirm_label = tk.Label(self, text="Are you sure you want to end the turn?", font=(None, 8, "bold"))
        self._confirm_label.grid(row=current_row, column=0, columnspan=2)
        current_row += 1
        self._cancel_btn = tk.Button(self, text="Cancel", command=self._close_window_callback)
        self._cancel_btn.grid(row=current_row, column=0)
        self._confirm_btn = tk.Button(self, text="Confirm", command=self._confirm)
        self._confirm_btn.grid(row=current_row, column=1)

    def _confirm(self):
        self._confirm_btn_callback()
        self._close_window_callback()

