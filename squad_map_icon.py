# squad_map_icon.py
#
# Wrapper class for squad buttons in SquadMenu

import tkinter as tk


class SquadMapIcon(tk.Frame):

    def __init__(self, master, squad, squad_menu_callback, fighter_icon):
        super(SquadMapIcon, self).__init__(master)

        self._master = master
        self._squad = squad
        self._squad_menu_callback = squad_menu_callback
        self._fighter_icon = fighter_icon
        self._create_widgets()


    def _create_widgets(self):
        self._icon = tk.Label(self, image=self._fighter_icon, borderwidth=2, relief="groove")
        self._icon.pack()
        # self._icon.bind("<Button-1>", self._show_squad_menu)


    # def _show_squad_menu(self, event):
    #     self._squad_menu_callback(self._squad, event)

    def set_relief(self, relief_var):
        self._icon.config(relief=relief_var)

    def disable(self):
        print("Disabling icon...")
        self._icon.config(state="disabled")

    def enable(self):
        self._icon.config(state="normal")