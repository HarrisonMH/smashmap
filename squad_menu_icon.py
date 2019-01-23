# squad_menu_icon.py
#
# Wrapper class for squad buttons in SquadMenu

import tkinter as tk


class SquadMenuIcon(tk.Frame):

    def __init__(self, master, squad, squad_menu_callback, fighter_icon):
        super(SquadMenuIcon, self).__init__(master)

        self._master = master
        self._squad = squad
        self._squad_menu_callback = squad_menu_callback
        self._fighter_icon = fighter_icon
        self._create_widgets()


    def _create_widgets(self):
        self._icon = tk.Label(self, image=self._fighter_icon, borderwidth=2, relief="groove")
        if self._squad.get_turn_status():
            self._icon.config(state="disabled")
        self._icon.pack()
        self._icon.bind("<Button-1>", self._show_squad_menu)


    def _show_squad_menu(self, event):
        self._squad_menu_callback(self._squad, event)

    def set_relief(self, relief_var):
        self._icon.config(relief=relief_var)