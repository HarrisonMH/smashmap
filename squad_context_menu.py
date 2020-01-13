# squad_context_menu.py
#
# Defines layout, attributes and methods for SquadContextMenu; accessed when right-clicking on a selected squad

import tkinter as tk


class SquadContextMenu(tk.Frame):
    def __init__(self, master, squad, canvas_item_id, destroy_squad_context_menu_callback, **kwargs):
        super().__init__(master, kwargs)

        self._squad = squad
        self._canvas_item_id = canvas_item_id
        self._destroy_squad_context_menu_callback = destroy_squad_context_menu_callback
        self._create_widgets()

    def _create_widgets(self):
        button_width = 8
        if self._squad.get_location().get_owner() is None:
            self._build_btn = tk.Button(self, text="Build", width=button_width, overrelief="groove", command=self._context_colonize)
            self._build_btn.pack()
        self._pass_btn = tk.Button(self, text="Pass", width=button_width, overrelief="groove", command=self._context_pass)
        self._pass_btn.pack()
        self._cancel_btn = tk.Button(self, text="Cancel", width=button_width, overrelief="groove", command=self.destroy)
        self._cancel_btn.pack()

    def _context_colonize(self):
        self._squad.colonize()
        self._destroy_squad_context_menu_callback(self._canvas_item_id)
        # self.destroy()

    def _context_pass(self):
        self._squad.pass_action()
        self._squad.get_location().unhighlight_adjacent_hexes()
        self._squad.get_owner().get_main_window().next_player()
        self._destroy_squad_context_menu_callback(self._canvas_item_id)
        # self.destroy()

    def mouse_exit(self, event):
        print("Mouse left context")
        self._destroy_squad_context_menu_callback(self._canvas_item_id)
