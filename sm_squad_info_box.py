# sm_squad_info_box
#
# Widget for displaying squad stats in the side menu

import tkinter as tk


class SquadInfoBox(tk.Frame):
    def __init__(self, master, squad, fighter_image_dict, icon_image_dict, **kwargs):
        super().__init__(master, kwargs)

        self._master = master
        # self._squad = squad
        self._fighter_image_dict = fighter_image_dict
        self._icon_image_dict = icon_image_dict

        self._fighter_var = tk.StringVar()
        self._kills_var = tk.StringVar()
        self._bounty_var = tk.StringVar()

        # self._squad_image = ""

        self._create_widgets()
        self.update_display(squad)

    def _create_widgets(self):
        current_row = 0
        self._squad_icon_frame = tk.Frame(self, width=50, height=50)
        # Prevent icon from resizing the frame
        self._squad_icon_frame.pack_propagate(0)
        self._squad_icon_label = tk.Label(self._squad_icon_frame, image="", relief="ridge", height=50, width=50)
        self._squad_icon_label.pack()
        self._squad_icon_frame.grid(row=current_row, column=0, columnspan=2)
        current_row += 1
        self._squad_fighter_label = tk.Label(self, textvariable=self._fighter_var, font=(None, 10, "bold"), wraplength=75, height=2)
        self._squad_fighter_label.grid(row=current_row, column=0, columnspan=2)
        current_row += 1
        self._squad_stats_box_row = current_row
        sub_row = 0
        self._squad_stats_box = tk.Frame(self)
        self._squad_kills_label = tk.Label(self._squad_stats_box, image=self._icon_image_dict["knife"]["map"], textvariable=self._kills_var, compound="left")
        self._squad_kills_label.grid(row=sub_row, column=0, columnspan=2)
        sub_row += 1
        self._vp_icon_label = tk.Label(self._squad_stats_box, text="VP", font=(None, 13, "bold"))
        self._vp_icon_label.grid(row=sub_row, column=0, sticky="E")
        self._vp_text_label = tk.Label(self._squad_stats_box, textvariable=self._bounty_var, font=(None, 10))
        self._vp_text_label.grid(row=sub_row, column=1, sticky="W")

    def update_display(self, squad):
        if squad is not None:
            squad_image = self._fighter_image_dict[squad.get_fighter()]["menu"]
            self._fighter_var.set(squad.get_fighter())
            self._kills_var.set(squad.get_kills())
            self._bounty_var.set(squad.get_bounty())
            self._squad_stats_box.grid(row=self._squad_stats_box_row, column=0, columnspan=2)
        else:
            squad_image = ""
            self._fighter_var.set("None")
            self._squad_stats_box.grid_forget()
        self._squad_icon_label.config(image=squad_image)

