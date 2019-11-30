# battle_popup.py
#
# Defines attributes, methods, and layout for the dialog popup that occurs when a squad attempts to enter a space with an enemy squad

import tkinter as tk


class BattlePopup(tk.Toplevel):

    def __init__(self, master, atk_squad, def_hex, fighter_image_dict, close_battle_popup_callback, hex_map_ref):
        super().__init__(master, borderwidth=4, relief="raised")
        self._atk_squad = atk_squad
        self._def_hex = def_hex
        self._fighter_image_dict = fighter_image_dict
        self._close_battle_popup = close_battle_popup_callback
        self._hex_map_ref = hex_map_ref
        self._def_squads = def_hex.get_squads()
        self._def_count = len(self._def_squads)
        self._def_select = None

        self._create_widgets()

    def _create_widgets(self):
        # self = tk.Toplevel(self, borderwidth=4, relief="raised")
        self.title("BATTLE!")
        self.geometry("+400+300")
        self.resizable(False, False)
        # self.overrideredirect(True)
    
        atk_player = self._atk_squad.get_owner()
        def_player = self._def_hex.get_squads()[0].get_owner()
        current_row = 0
        header_string = "BATTLE IN HEX " + str(self._def_hex.get_id()) + "!"
        self._heading = tk.Label(self, text=header_string, font=(None, 20, "bold"))
        self._heading.grid(row=current_row, column=0, columnspan=6)
        current_row += 1
        self._atk_header = tk.Label(self, text="ATTACKER", font=(None, 16))
        self._atk_header.grid(row=current_row, column=0, columnspan=2)
        self._def_header = tk.Label(self, text="DEFENDER", font=(None, 16))
        self._def_header.grid(row=current_row, column=4, columnspan=2)
        current_row += 1

        self._atk_name = tk.Label(self, text=atk_player.get_name(), width=15, font=(None, 16),
                                  bg=atk_player.get_colour(), borderwidth=3, relief="solid")
        self._atk_name.grid(row=current_row, column=0, columnspan=2, padx=5, pady=5)
        self._def_name = tk.Label(self, text=def_player.get_name(), width=15, font=(None, 16),
                                  bg=def_player.get_colour(), borderwidth=3, relief="solid")
        self._def_name.grid(row=current_row, column=4, columnspan=2, padx=5, pady=5)
        current_row += 1

        if len(self._def_hex.get_squads()) == 1:
            def_col_width = 2
        else:
            def_col_width = 1
            self._def_select_label = tk.Label(self, text="Select Defending Squad:", font=(None, 12, "bold"))
            self._def_select_label.grid(row=current_row, column=4, columnspan=2)
            current_row += 1

        attacker_image = self._fighter_image_dict[self._atk_squad.get_fighter()]["battle"]
        self._attacker_icon = tk.Label(self, image=attacker_image)
        self._attacker_icon.grid(row=current_row, column=1, padx=5)
        self._vs_label = tk.Label(self, text="VS.", font=(None, 40))
        self._vs_label.grid(row=current_row, column=2, columnspan=2, padx=5, pady=10)
        current_col = 4

        self._def_squads_icons = []

        # def_squads = self._def_hex.get_squads()

        self._v_defender = tk.IntVar()
        squad_num = 0
        for def_squad in self._def_squads:
            def_squad_image = self._fighter_image_dict[def_squad.get_fighter()]["battle"]
            if self._def_count == 2:
                self._def_squads_icons.append(tk.Radiobutton(self, indicatoron=0, image=def_squad_image,
                                                             variable=self._v_defender, value=squad_num, borderwidth=3,
                                                             command=self._select_defending_squad))
                squad_num += 1
            else:
                self._def_squads_icons.append(tk.Label(self, image=def_squad_image))
            self._def_squads_icons[-1].grid(row=current_row, column=current_col, columnspan=def_col_width, padx=5, pady=10)
            current_col += 1
        if self._def_count == 2:
            self._def_squads_icons[0].deselect()

        current_row += 1

        self._v_victor = tk.IntVar()
        self._victory_select_attacker = tk.Radiobutton(self, indicatoron=0, text=self._atk_squad.get_fighter(),
                                                       variable=self._v_victor, value=0, font=(None, 14),
                                                       command=self._select_wining_squad)
        self._victory_select_attacker.grid(row=current_row, column=0, columnspan=2, padx=5, pady=10)
        self._victor_label = tk.Label(self, text="Select Winner", font=(None, 16))
        self._victor_label.grid(row=current_row, column=2, columnspan=2, padx=5, pady=10)
        self._victory_select_defender = tk.Radiobutton(self, indicatoron=0, variable=self._v_victor, value=1,
                                                       font=(None, 14), command=self._select_wining_squad)
        if self._def_count == 1:
            self._victory_select_defender.config(text=self._def_squads[0].get_fighter())
        elif self._def_count == 2:
            self._victory_select_attacker.config(state="disabled")
            self._victory_select_defender.config(text="Select Defending Squad", state="disabled")
        self._victory_select_defender.grid(row=current_row, column=4, columnspan=2, padx=5, pady=10)

        current_row += 1

        self._cancel_btn = tk.Button(self, text="Cancel", command=self._close_battle_popup)
        self._cancel_btn.grid(row=current_row, column=2, padx=5, pady=10)
        self._confirm_btn = tk.Button(self, text="Confirm", state="disabled", command=self._resolve_battle)
        self._confirm_btn.grid(row=current_row, column=3, padx=5, pady=10)

    def _select_defending_squad(self):
        self._victory_select_attacker.config(state="normal")
        self._victory_select_defender.config(state="normal", text=self._def_squads[self._v_defender.get()].get_fighter())

    def _select_wining_squad(self):
        self._confirm_btn.config(state="normal")

    def _resolve_battle(self):
        if self._v_victor.get() == 0:
            self._def_squads[self._v_defender.get()].destroy_squad()
            # FIXME: Increment squad kill count
            if len(self._def_hex.get_squads()) == 0:
                self._atk_squad.move_squad(self._def_hex.get_id(), self._hex_map_ref, "hex")
            else:
                self._atk_squad.take_turn()
        elif self._v_victor.get == 1:
            self._atk_squad.destroy_squad()
            # FIXME: Increment squad kill count
                
        self._close_battle_popup()
