# squad_menu.py
#
# Define attributes of SquadMenu class, which is a sub-menu of the Player_menu

import tkinter as tk
from move_button import MoveButton


class SquadMenu(tk.Frame):

    def __init__(self, master, squad, hex_map, parent_menu_str):
        super(SquadMenu, self).__init__(master)

        self._master = master
        self._squad = squad
        self._hex_map_ref = hex_map
        self._parent_menu_str = parent_menu_str
        self._move_buttons = []

        self._create_widgets()


    def _create_widgets(self):
        current_row=0
        self._header = tk.Label(self, text="Squad Info", font=(None, 16))
        self._header.grid(row=current_row, column=0, columnspan=5)
        current_row += 1
        # self._id_label = tk.Label(self, text="Squad ID: " + str(self._squad.get_squad_id()))
        # self._id_label.grid(row=current_row, column=0)
        # current_row += 1
        self._fighter_label = tk.Label(self, text="Fighter: " + self._squad.get_fighter(), font=(None, 12))
        self._fighter_label.grid(row=current_row, column=0, padx=(1, 20))
        self._owner_label = tk.Label(self, text="Owner: " + self._squad.get_owner_name(), font=(None, 12))
        self._owner_label.grid(row=current_row, column=2)
        current_row += 1
        self._loc_label = tk.Label(self, text="Location: Hex " + str(self._squad.get_location().get_id()), font=(None, 12))
        self._loc_label.grid(row=current_row, column=0)
        self._kill_count = tk.Label(self, text="Kills: " + str(self._squad.get_kills()), font=(None, 12))
        self._kill_count.grid(row=current_row, column=2)
        current_row += 1
        self._subheader = tk.Label(self, text="Available Actions", font=(None, 14))
        self._subheader.grid(row=current_row, column=0, columnspan=5, pady=5)
        current_row += 1
        self._move_btn = tk.Button(self, text="Move", font=(None, 10, "bold"), command=self._generate_move_list)
        self._move_btn.grid(row=current_row, column=0, pady=(1, 10))
        self._build_btn = tk.Button(self, text="Build", font=(None, 10, "bold"), command=self._colonize)
        self._build_btn.grid(row=current_row, column=2, pady=(1, 10))
        current_row += 1
        self._delete_btn = tk.Button(self, text="Delete Squad", font=(None, 10, "bold"), command=self._delete_squad)
        self._delete_btn.grid(row=current_row, column=2, pady=(1, 10))
        current_row += 1
        self._action_menu = tk.Frame(self)


    def _generate_move_list(self):
        self._move_btn.config(relief="sunken")
        self._action_menu.grid_forget()
        hex_list = self._hex_map_ref.get_hex_list()
        squad_loc = self._squad.get_location()
        # adj_hexes = hex_list[squad_loc - 1].get_adjacent_ids()
        adj_hexes = squad_loc.get_adjacent_ids()
        #FIXME: Add logic to check for space in adjacent hexes

        self._move_menu = tk.Frame(self)

        for i, hex_id in enumerate(adj_hexes):
            adj_hex = hex_list[hex_id - 1]
            adj_squads = adj_hex.get_squads()
            bg_color = None
            btn_state = "normal"
            for squad in adj_squads:
                if squad.get_owner_name() != self._squad.get_owner_name():
                    bg_color = "red"
                # FIXME: Check why squad cannot move back into HQ after first move - triggerd by second term in OR clause below
                if (not adj_hex.check_open_space()) or (adj_hex.get_structure() == "HQ" and adj_hex.get_owner != self._squad.get_owner()):
                    btn_state = "disabled"
            self._move_buttons.append(MoveButton(self._move_menu, hex_id, self._parent_menu_str, self._hex_map_ref,
                                                 self._squad.move_squad, text=str(hex_id), background=bg_color, state=btn_state))
            self._move_buttons[-1].grid(row=0, column=i)
        self._action_menu = self._move_menu
        self._action_menu.grid(row=15, column=0)


    def _colonize(self):
        current_loc = self._squad.get_location()
        if current_loc.get_owner() is None:
            current_loc.change_owner(self._squad.get_owner(), self._squad.get_owner().get_colour())
            self._squad.take_turn()
            self._squad.get_owner().adjust_territory_size(1)
            self._squad.get_owner().adjust_income(current_loc.get_value())
            self._squad.get_owner().adjust_vp_income(current_loc.get_vp_value())
            self._squad.refresh_active_menu(self._parent_menu_str)


    def _move_click(self, event):
        event.widget.config(relief="sunken")
        new_loc_id = int(event.widget.cget("text"))
        self._squad.move_squad(new_loc_id, self._hex_map_ref, self._parent_menu_str)
        self._move_btn.config(relief="raised")
        self._action_menu.grid_forget()


    def _release_button(self, event):
        event.widget.config(relief="raised")


    def _delete_squad(self):
        self._squad.destroy_squad(self._parent_menu_str)
