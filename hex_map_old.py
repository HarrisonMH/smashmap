# hex_map.py
#
#
#
#

import tkinter as tk
import math
from hex import Hex

COS_30 = math.cos(math.radians(30))
SIN_30 = math.sin(math.radians(30))

class HexMap(tk.Frame):

    def __init__(self, master, parent, size, hex_menu_callback):
        super().__init__(master)
        self._master = master
        self._parent = parent
        self.hex_grid = tk.Canvas(self, height=780, width=1275, bg="black")
        self.hex_grid.grid(column=0, row=1)
        self._hex_menu_callback = hex_menu_callback

        self._hex_ids = []
        self._hexes = []

        self._create_grid(size)
        self._label_grid()


    def _create_grid(self, size):
        start_x = 50
        curr_x = start_x
        curr_y = 50
        margin = 5
        x_offset = start_x + (COS_30 * start_x) + 3
        for row in range(9):
            print("Generating row " + str(row))
            if row % 2 == 0:
                for hex in range(13):
                    next_hex = self._create_hex(curr_x, curr_y, size)
                    curr_x = next_hex[0] + margin
            else:
                for hex in range(12):
                    next_hex = self._create_hex(curr_x, curr_y, size)
                    curr_x = next_hex[0] + margin
            if row % 2 == 0:
                curr_x = x_offset
            else:
                curr_x = start_x
            curr_y = curr_y + (COS_30 * start_x * 2) - 7


    def _create_hex(self, start_x, start_y, size):
        hex_points = self._calculate_hex_points(start_x, start_y, size)
        hex_id = self.hex_grid.create_polygon(hex_points[0][0], hex_points[0][1], hex_points[1][0], hex_points[1][1], hex_points[2][0], hex_points[2][1], hex_points[3][0], hex_points[3][1], hex_points[4][0], hex_points[4][1], hex_points[5][0], hex_points[5][1], outline="white", activedash=True)
        self._hex_ids.append(hex_id)
        self._hexes.append(Hex(self.hex_grid, self._master, self, hex_id, self._hex_menu_callback))
        return hex_points[2]


    def _label_grid(self):
        print("Laebeling grid...")
        for hex in self._hex_ids:
            label = str(hex)
            # print("Adding label " + label)
            coords = self.hex_grid.coords(hex)
            self.hex_grid.create_text((coords[0] + coords[4]) / 2, coords[1] - 10, fill="white", text=label, justify="center")


    def _calculate_hex_points(self, start_x, start_y, size):
        # print("Creating hex: " + str(start_x), str(start_y), str(size))
        p1 = (start_x, start_y)
        p2 = (start_x + (COS_30 * size), (start_y + (SIN_30 * size * -1)))
        p3 = ((p2[0] + (COS_30 * size)), start_y)
        p4 = (p3[0], start_y + size)
        p5 = (p2[0], p4[1] + (SIN_30 * size))
        p6 = (start_x, start_y + size)
        return (p1, p2, p3, p4, p5, p6)


    def initialize_start_positions(self, player_data):
        start_positions = [1, 7, 13, 101, 107, 113]
        current_player = 1
        for hex in start_positions:
            self._parent._players[current_player-1].set_hq(hex)
            current_player_str = "p" + str(current_player)
            current_player_data = player_data[current_player_str]
            self._hexes[hex - 1].change_owner(current_player_data)
            current_player += 1
