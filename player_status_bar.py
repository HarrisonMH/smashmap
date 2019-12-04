# player_status_bar.py
#
# Defines attributes, methods and layout for player status menu

import tkinter as tk


class PlayerStatusBar(tk.Frame):
    def __init__(self, master, player, icon_image_dict, **kwargs):
        super().__init__(master, kwargs)

        self._player = player
        self._player.set_status_bar_ref(self)
        self._player_label_str = "Player " + str(self._player.get_player_number()) + ": " + self._player.get_name()
        self._icon_image_dict = icon_image_dict
        self._create_widgets()


    def _create_widgets(self):
        current_row = 0
        self._player_label = tk.Label(self, width=11, text=self._player_label_str, font=(None, 14), fg="white",
                                      bg=self._player.get_colour(), borderwidth=4, relief="groove")
        self._player_label.grid(row=current_row, column=0, columnspan=5, padx=10, sticky="W"+"E")
        current_row += 1
        self._hq_icon_label = tk.Label(self, image=self._icon_image_dict["hq"]["map"])
        self._hq_icon_label.grid(row=current_row, column=0, sticky="E")
        self._hq_text_label = tk.Label(self, text=str(self._player.get_hq().get_id()), font=(None, 10))
        self._hq_text_label.grid(row=current_row, column=1, sticky="W")
        self._territory_icon_label = tk.Label(self, image=self._icon_image_dict["hex_hollow"]["map"])
        self._territory_icon_label.grid(row=current_row, column=3, sticky="E")
        self._territory_text_label = tk.Label(self, text=str(self._player.get_territory_size()), font=(None, 10))
        self._territory_text_label.grid(row=current_row, column=4, sticky="W")
        current_row += 1
        self._vp_icon_label = tk.Label(self, text="VP", font=(None, 14, "bold"))
        self._vp_icon_label.grid(row=current_row, column=0, sticky="E")
        self._vp_text_label = tk.Label(self, text=str(self._player.get_vp()), font=(None, 10))
        self._vp_text_label.grid(row=current_row, column=1, sticky="W")
        self._vp_income_icon_label = tk.Label(self, image=self._icon_image_dict["income"]["map"])
        self._vp_income_icon_label.grid(row=current_row, column=3, sticky="E")
        self._vp_income_text_label = tk.Label(self, text=str(self._player.get_vp_income()), font=(None, 10))
        self._vp_income_text_label.grid(row=current_row, column=4, sticky="W")
        current_row += 1
        self._res_icon_label = tk.Label(self, image=self._icon_image_dict["dollar"]["map"])
        self._res_icon_label.grid(row=current_row, column=0, sticky="E")
        self._res_text_label = tk.Label(self, text=str(self._player.get_resources()), font=(None, 10))
        self._res_text_label.grid(row=current_row, column=1, sticky="W")
        self._res_income_icon_label = tk.Label(self, image=self._icon_image_dict["income"]["map"])
        self._res_income_icon_label.grid(row=current_row, column=3, sticky="E")
        self._res_income_text_label = tk.Label(self, text=str(self._player.get_income()), font=(None, 10))
        self._res_income_text_label.grid(row=current_row, column=4, sticky="W")

    def set_territory_size(self, value):
        self._territory_text_label.config(text=str(value))

    def set_vp(self, value):
        self._vp_text_label.config(text=value)

    def set_vp_income(self, value):
        self._vp_income_text_label.config(text=value)

    def set_res(self, value):
        self._res_text_label.config(text=value)

    def set_res_income(self, value):
        self._res_income_text_label.config(text=value)

    def get_owner(self):
        return self._player

