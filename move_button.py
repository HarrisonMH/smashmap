# move_button.py
#
# Defines attributes and methods for the buttons that appear when moving a squad

import tkinter as tk


class MoveButton(tk.Button):

    def __init__(self, master, new_loc_id, parent_menu_str, hex_map_ref, move_squad_callback, **kwargs):
        super().__init__(master, kwargs, command=self._move_squad)

        self._new_loc_id = new_loc_id
        self._parent_menu_str = parent_menu_str
        self._hex_map_ref = hex_map_ref
        self._move_squad_callback = move_squad_callback

    def _move_squad(self):
        self._move_squad_callback(self._new_loc_id, self._hex_map_ref, self._parent_menu_str)

