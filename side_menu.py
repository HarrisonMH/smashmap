# side_menu.py
#
# Defines layout, attributes and methods for unified side menu

import tkinter as tk
import tkinter.ttk as ttk

# FIXME: Add play log to bottom of menu, implement hiding logic for non-applicable elements
class SideMenu(tk.Frame):
    def __init__(self, master, main_window_ref, hex, hex_map, fighter_image_dict, fighter_list, icon_image_dict, **kwargs):
        super().__init__(master, kwargs)
        self._master = master
        self._main_window_ref = main_window_ref
        self._hex = hex
        self._hex_map = hex_map
        self._fighter_image_dict = fighter_image_dict
        self._fighter_list = fighter_list
        self._icon_image_dict = icon_image_dict

        self._hex_owner = self._hex.get_owner()
        self._squads = None

        self._player_num_str_var = tk.StringVar()
        self._player_name_var = tk.StringVar()
        self._player_colour_str = "white"
        self._hex_id_str_var = tk.StringVar()
        self._vp_str_var = tk.StringVar()
        self._structure_image = None
        self._structure_str_var = tk.StringVar()
        self._structure_effect_var = tk.StringVar()
        self._res_str_var = tk.StringVar()
        self._squad_picker_var = tk.StringVar()
        self._squad_picker_var.trace("w", self._squad_picker_update_callback)

        self._sq1_image = None
        self._sq1_fighter_var = tk.StringVar()
        self._sq1_kills_str_var = tk.StringVar()
        self._sq1_state = "normal"
        # FIXME: Refactor squads for VP value
        # self._sq1_vp_var = tk.StringVar()
        self._sq2_image = None
        self._sq2_fighter_var = tk.StringVar()
        self._sq2_kills_str_var = tk.StringVar()
        self._sq2_state = "normal"
        # self._sq2_vp_var = tk.StringVar()
        self._allow_build = False

        self.set_new_values(hex)

        print("Generating Side Menu...")
        self._create_widgets()

        self.update_non_var_values()

    def _create_widgets(self):
        current_row = 0
        # Player header widgets
        self._player_num_header = tk.Label(self, width=20, textvariable=self._player_num_str_var, font=(None, 16))
        self._player_num_header.grid(row=0, column=0, columnspan=4)
        current_row += 1
        self._player_name_header = tk.Label(self, textvariable=self._player_name_var, width=10, font=(None, 16),
                                            bg=self._player_colour_str, borderwidth=2, relief="solid")
        self._player_name_header.grid(row=current_row, column=0, columnspan=4, pady=(1, 10))
        current_row += 1

        # Hex header widgets
        self._header = tk.Label(self, textvariable=self._hex_id_str_var, font=(None, 16))
        self._header.grid(row=current_row, column=0, columnspan=4, pady=(1, 10))
        current_row += 1
        self._vp_symbol_label = tk.Label(self, text="VP", font=(None, 14, "bold"))
        self._vp_symbol_label.grid(row=current_row, column=0, sticky="e")
        self._vp_value_label = tk.Label(self, textvariable=self._vp_str_var, font=(None, 12))
        self._vp_value_label.grid(row=current_row, column=1, sticky="w")
        self._res_label = tk.Label(self, image=self._icon_image_dict["dollar"]["map"], textvariable=self._res_str_var, font=(None, 12), compound="left")
        self._res_label.grid(row=current_row, column=2, columnspan=2, sticky="w")
        current_row += 1

        # Structure info widgets
        structure = self._hex.get_structure()
        if structure is not None:
            self._structure_image_label = tk.Label(self, image=self._icon_image_dict[structure.lower()]["menu"])
            self._structure_image_label.grid(row=current_row, column=0, columnspan=4)
            current_row += 1
            self._structure_text_label = tk.Label(self, textvariable=self._structure_str_var, font=(None, 16))
            self._structure_text_label.grid(row=current_row, column=0, columnspan=4)
            current_row += 1
            self._structure_effect_label = tk.Label(self, textvariable=self._structure_effect_var, font=(None, 12))
            self._structure_effect_label.grid(row=current_row, column=0, columnspan=4)
        current_row += 1

        # Build widgets
        self._build_squad_label = tk.Label(self, text="New squad: ", state="disabled")
        self._build_squad_label.grid(row=current_row, column=0, columnspan=1, pady=10)
        self._build_squad_picker = ttk.Combobox(self, textvariable = self._squad_picker_var, values=self._fighter_list, state="disabled")
        self._build_squad_picker.grid(row=current_row, column=1, columnspan=3, pady=10, padx=10)
        current_row += 1
        self._build_squad_btn = tk.Button(self, text="Build", font=(None, 10, "bold"), state="disabled",
                                          command=self._build_new_squad)
        self._build_squad_btn.grid(row=current_row, column=0, columnspan=4, pady=10, padx=10, sticky="w"+"e")
        current_row += 1

        # Squad widgets
        self._squads_header_label = tk.Label(self, text="Squads", font=(None, 16))
        self._squads_header_label.grid(row=current_row, column=0, columnspan=4, pady=(10, 0))
        current_row += 1
        self._squad_1_icon_label = tk.Label(self, image=self._sq1_image)
        self._squad_1_icon_label.grid(row=current_row, column=0, columnspan=2)
        self._squad_2_icon_label = tk.Label(self, image=self._sq2_image)
        self._squad_2_icon_label.grid(row=current_row, column=2, columnspan=2)
        current_row += 1
        self._squad_1_fighter_label = tk.Label(self, textvariable=self._sq1_fighter_var, font=(None, 10, "bold"), wraplength=75)
        self._squad_1_fighter_label.grid(row=current_row, column=0, columnspan=2)
        self._squad_2_fighter_label = tk.Label(self, textvariable=self._sq2_fighter_var, font=(None, 10, "bold"), wraplength=75)
        self._squad_2_fighter_label.grid(row=current_row, column=2, columnspan=2)
        current_row += 1
        self._squad_1_kills_label = tk.Label(self, image=self._icon_image_dict["knife"]["map"],
                                             textvariable=self._sq1_kills_str_var, compound="left")
        self._squad_1_kills_label.grid(row=current_row, column=0, columnspan=2)
        self._squad_2_kills_label = tk.Label(self, image=self._icon_image_dict["knife"]["map"],
                                             textvariable=self._sq2_kills_str_var, compound="left")
        self._squad_2_kills_label.grid(row=current_row, column=2, columnspan=2)

    def get_structure_effect_str(self, structure):
        structure_str = ""
        if structure == "Mine":
            structure_str = "(+25 Res. +1 VP)"
        elif structure == "Factory":
            structure_str = "(Build)"
        elif structure == "Refinery":
            structure_str = "(+175 Res, +5 VP)"
        elif structure == "HQ":
            structure_str = "(+150 Res, Fast Build)"
        return structure_str

    def set_new_values(self, hex):
        self._hex = hex
        self._hex_owner = hex.get_owner()
        if self._hex_owner is not None:
            self._player_num_str_var.set("Player " + str(self._hex_owner.get_player_number()))
            self._player_name_var.set(self._hex_owner.get_name())
            self._player_colour_str = self._hex_owner.get_colour()
        else:
            self._player_num_str_var.set("Unclaimed Hex")
            self._player_name_var.set("")
            self._player_colour_str = "white"
        self._hex_id_str_var.set("Hex " + str(hex.get_id()))
        self._vp_str_var.set(hex.get_vp_value())
        self._res_str_var.set(hex.get_value())

        structure = self._hex.get_structure()
        if structure is not None:
            self._structure_image = self._icon_image_dict[structure.lower()]["menu"]
            self._structure_str_var.set("Structure: " + structure)
            self._structure_effect_var.set(self.get_structure_effect_str(structure))
            if (structure == "HQ" or structure == "Factory") and self._hex_owner is not None:
                self.set_allow_build(True)
            else:
                self.set_allow_build(False)
        else:
            self._structure_image = ""
            self._structure_str_var.set("")
            self._structure_effect_var.set("")
        self._squads = hex.get_squads(False)
        if self._squads[0] is not None:
            self._sq1_fighter_var.set(self._squads[0].get_fighter())
            self._sq1_kills_str_var.set(self._squads[0].get_kills())
            self._sq1_image = self._fighter_image_dict[self._squads[0].get_fighter()]["menu"]
            if self._squads[0].get_turn_status() is False:
                self._sq1_state = "normal"
            elif self._squads[0].get_turn_status() is True:
                self._sq1_state = "disabled"
        else:
            self._sq1_fighter_var.set(None)
            self._sq1_kills_str_var.set(None)
            self._sq1_image = ""
        if self._squads[1] is not None:
            self._sq2_fighter_var.set(self._squads[1].get_fighter())
            self._sq2_kills_str_var.set(self._squads[1].get_kills())
            self._sq2_image = self._fighter_image_dict[self._squads[1].get_fighter()]["menu"]
            if self._squads[1].get_turn_status() is False:
                self._sq2_state = "normal"
            elif self._squads[1].get_turn_status() is True:
                self._sq2_state = "disabled"
        else:
            self._sq2_fighter_var.set(None)
            self._sq2_kills_str_var.set(None)
            self._sq2_image = ""

    def set_allow_build(self, value):
        self._allow_build = value

    def update_non_var_values(self):
        self._player_name_header.config(bg=self._player_colour_str)
        self._structure_image_label.config(image=self._structure_image)
        self._squad_1_icon_label.config(image=self._sq1_image, state=self._sq1_state)
        self._squad_2_icon_label.config(image=self._sq2_image, state=self._sq2_state)

        current_player = self._main_window_ref.get_current_player()
        structure = self._hex.get_structure()
        squad_build_state = "disabled"
        squad_picker_state = "disabled"
        if structure == "HQ" or structure == "Factory":
            # FIXME: Add conditional display logic for Build widgets
            if self._allow_build is True and self._hex_owner == current_player:
                squad_build_state = "normal"
                squad_picker_state = "readonly"
        self._build_squad_label.config(state=squad_build_state)
        self._build_squad_btn.config(state=squad_build_state)
        self._build_squad_picker.config(state=squad_picker_state)
        self._squad_picker_var.set("")

    def update_all(self, hex):
        # FIXME: Update selected hex when advancing to next player
        self.set_new_values(hex)
        self.update_non_var_values()

    # FIXME: Add cost multiplication logic for building duplicate squads
    def _build_new_squad(self):
        fighter = self._build_squad_picker.get()
        if fighter != "":
            self._hex.get_owner().build_squad(fighter, self._hex)
            self.update_all(self._hex)

    def _squad_picker_update_callback(self, var, index, mode):
        print("Picker updated:", self._squad_picker_var.get())
        # print("Var name:", var)
        # print("Var index (if var is iterable):", index)
        # print("Mode:", mode)
        if self._hex_owner is not None and self._squad_picker_var.get() != "":
            squad_cost = self._hex_owner.get_new_squad_cost(self._squad_picker_var.get())
            self._build_squad_btn.config(text="Build " + "(" + str(squad_cost) + ")")
        else:
            self._build_squad_btn.config(text="Build")


