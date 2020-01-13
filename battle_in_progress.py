# battle_in_progress.py
#
# Defines the Battle in Progress status box, created when clicking "defer"

import tkinter as tk


class BattleInProgress(tk.Frame):
    def __init__(self, master, atk_squad, def_squad, close_window_callback, **kwargs):
        super().__init__(master, kwargs)

        self._atk_squad = atk_squad
        self._def_squad = def_squad
        self._atk_player = self._atk_squad.get_owner()
        self._def_player = self._def_squad.get_owner()

        self._close_window_callback = close_window_callback

        self._create_widgets()

    def _create_widgets(self):
        current_row = 0
        self._atk_name_label = tk.Label(self, text=self._atk_player.get_name(), width=10, font=(None, 11),
                                        bg=self._atk_player.get_colour(), borderwidth=3, relief="solid")
        self._atk_name_label.grid(row=current_row, column=0, padx=5, pady=5)
        self._def_name_label = tk.Label(self, text=self._def_player.get_name(), width=10, font=(None, 11),
                                        bg=self._def_player.get_colour(), borderwidth=3, relief="solid")
        self._def_name_label.grid(row=current_row, column=2, padx=5, pady=5)
        current_row += 1
