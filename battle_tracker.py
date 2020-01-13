# battle_tracker.py
#
# Status menu frame, container for BattleInProgress objects

import tkinter as tk
from battle_in_progress import BattleInProgress

class BattleTracker(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, kwargs)

        self._create_widgets()
        self._battles = []

    def _create_widgets(self):
        self._header_label = tk.Label(text="Battles In Progress", font=(None, 14, "bold"))
        self._header_label.pack()

    def new_battle(self, squad1, squad2):
        self._battles.append(BattleInProgress(self, squad1, squad2))
        self._battles[-1].pack()

    def _destroy_bip_callback(self, bip):
        pass