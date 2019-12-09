# colour_picker.py
#
# Defines the colour picker widget for player colour selection in the start menu

import tkinter as tk

VALID_COLOUR_LIST = ["brown", "red", "hotpink", "darkorange", "goldenrod", "lime", "green", "darkcyan", "royalblue",
                     "purple", "mediumslateblue", "wheat"]


class ColourPicker(tk.Frame):
    def __init__(self, master, default_value=0, **kwargs):
        super().__init__(master, kwargs)
        self._master = master
        self._colour_var = tk.StringVar()
        self._default_value = VALID_COLOUR_LIST[default_value]
        self._colour_var.set(self._default_value)
        self._create_widgets()

    def _create_widgets(self):
        self._current_selection_label = tk.Button(self, bg=self._colour_var.get(), command=self._colour_select_popup, height=1, width=15)
        self._current_selection_label.grid(row=0, column=0)
        self._master.change_selected_colours(self._colour_var.get())

    def _colour_select_popup(self):
        widget_x = str(self._current_selection_label.winfo_rootx())
        widget_y = str(self._current_selection_label.winfo_rooty())
        print("+{}+{}".format(widget_x, widget_y))
        self._colour_select_menu = tk.Toplevel(self)
        self._colour_select_menu.geometry("+{}+{}".format(widget_x, widget_y))
        self._colour_select_menu.overrideredirect(True)
        # self._colour_select_frame = tk.Frame(self._colour_select_menu)
        self._colour_list = []
        current_row = 0
        current_col = 0
        for colour in VALID_COLOUR_LIST:
            # FIXME: Add some indication of disabled colour options
            self._colour_list.append(tk.Radiobutton(self._colour_select_menu, variable=self._colour_var, value=colour,
                                                    width=4, height=2, bg=colour, selectcolor=colour, indicatoron=0, command=self.select_colour))
            if colour in self._master.get_selected_colour_list():
                self._colour_list[-1].config(state="disabled")
            self._colour_list[-1].grid(row=current_row, column=current_col, padx=2, pady=2)
            if current_col == 3:
                current_row += 1
                current_col = 0
            else:
                current_col += 1
        # self._colour_select_menu.bind("<Leave>", self._mouse_exit)

    def select_colour(self):
        print(self._master.get_selected_colour_list())
        current_colour = self._current_selection_label.cget("bg")
        new_colour = self._colour_var.get()
        print(current_colour, new_colour)
        self._current_selection_label.config(bg=new_colour)
        self._master.change_selected_colours(new_colour, current_colour)
        self._colour_select_menu.destroy()

    def _mouse_exit(self, event):
        self._colour_select_menu.destroy()

    def get_colour(self):
        return self._colour_var.get()
