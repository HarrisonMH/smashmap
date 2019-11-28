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
TEST_WIDTH_50 = COS_30 * 100


class HexMap(tk.Frame):

    def __init__(self, master, parent, size, hex_menu_callback):
        super().__init__(master)
        self._master = master
        self._parent = parent
        self.hex_grid = tk.Canvas(self, height=780, width=900, bg="white")
        self.hex_grid.grid(column=0, row=1)
        self._hex_menu_callback = hex_menu_callback

        self._hex_coord_dict = {}
        self._hexes = []

        self._create_grid(size)
        # self._create_squad_slots()
        self._define_squad_slot_coords()
        self._create_structure_slots()
        self._label_grid()


    def _create_grid(self, size):
        start_x = (int(self.hex_grid.cget("width")) / 2) - (TEST_WIDTH_50 * 2.5)
        curr_x = start_x
        curr_y = 50
        margin = 5
        x_offset = (COS_30 * 50) + 3
        print("Generating grid...")
        for row in range(9):
            # print("Generating row " + str(row))
            if row == 0 or row == 8:
                for column in range(5):
                    next_hex = self._create_hex(curr_x, curr_y, size, row, column)
                    curr_x = next_hex[0] + margin
            elif row == 1 or row == 7:
                for column in range(6):
                    next_hex = self._create_hex(curr_x, curr_y, size, row, column)
                    curr_x = next_hex[0] + margin
            elif row == 2 or row == 6:
                for column in range(7):
                    next_hex = self._create_hex(curr_x, curr_y, size, row, column)
                    curr_x = next_hex[0] + margin
            elif row == 3 or row == 5:
                for column in range(8):
                    next_hex = self._create_hex(curr_x, curr_y, size, row, column)
                    curr_x = next_hex[0] + margin
            elif row == 4:
                for column in range(9):
                    next_hex = self._create_hex(curr_x, curr_y, size, row, column)
                    curr_x = next_hex[0] + margin
            if row < 4:
                curr_x = start_x - (x_offset * (row + 1))
            else:
                curr_x = start_x - (x_offset * (7 - row))
            curr_y = curr_y + (COS_30 * 50 * 2) - 7


    def _create_hex(self, start_x, start_y, size, row, column):
        hex_points = self._calculate_hex_points(start_x, start_y, size)
        hex_id = self.hex_grid.create_polygon(hex_points[0][0], hex_points[0][1], hex_points[1][0], hex_points[1][1],
                                              hex_points[2][0], hex_points[2][1], hex_points[3][0], hex_points[3][1],
                                              hex_points[4][0], hex_points[4][1], hex_points[5][0], hex_points[5][1],
                                              fill="white", outline="black", activedash=True, width=2)
        self._hex_coord_dict[hex_id] = hex_points
        adjacent_hexes = self._calculate_adjacency(row, column)
        # structure = "None"
        # if hex_id == 31:
        #     structure = "Refinery"
        self._hexes.append(Hex(self.hex_grid, self._master, self, hex_id, self._hex_menu_callback, row, column, adjacent_hexes))
        return hex_points[2]


    # def _create_squad_slots(self):
    #     for hex_id in self._hex_coord_dict:
    #         icon_1_x = self._hex_coord_dict[hex_id][0][0] + (TEST_WIDTH_50 / 4)
    #         icon_2_x = self._hex_coord_dict[hex_id][0][0] + (TEST_WIDTH_50 * 0.75)
    #         icon_y = self._hex_coord_dict[hex_id][0][1] + 25
    #         slot_1 = self.hex_grid.create_window((icon_1_x, icon_y))
    #         slot_2 = self.hex_grid.create_window((icon_2_x, icon_y))
    #         self._hexes[hex_id - 1].set_squad_slot_ids([slot_1, slot_2])
    #     return


    def _define_squad_slot_coords(self):
        for hex_id in self._hex_coord_dict:
            icon_1_x = self._hex_coord_dict[hex_id][0][0] + (TEST_WIDTH_50 / 4)
            icon_2_x = self._hex_coord_dict[hex_id][0][0] + (TEST_WIDTH_50 * 0.75)
            icon_y = self._hex_coord_dict[hex_id][0][1] + 25
            slot_1_coords = (icon_1_x, icon_y)
            slot_2_coords = (icon_2_x, icon_y)
            self._hexes[hex_id - 1].set_squad_slot_coords([slot_1_coords, slot_2_coords])
        return


    def _create_structure_slots(self):
        for hex_id in self._hex_coord_dict:
            slot_x = self._hex_coord_dict[hex_id][0][0] + (TEST_WIDTH_50 / 2)
            slot_y = self._hex_coord_dict[hex_id][4][1] - 20
            self._hexes[hex_id - 1].set_structure_coords([slot_x, slot_y])
        return


    def _label_grid(self):
        print("Labeling grid...")
        for hex in self._hexes:
            hex_id = hex.get_id()
            label = str(hex_id)
            coords = self.hex_grid.coords(hex_id)
            self.hex_grid.create_text((coords[0] + coords[4]) / 2, coords[1] - 10, fill="black", text=label, justify="center", font=(None, 8, "bold"))
        return


    def _calculate_hex_points(self, start_x, start_y, size):
        p1 = (start_x, start_y)
        p2 = (start_x + (COS_30 * size), (start_y + (SIN_30 * size * -1)))
        p3 = ((p2[0] + (COS_30 * size)), start_y)
        p4 = (p3[0], start_y + size)
        p5 = (p2[0], p4[1] + (SIN_30 * size))
        p6 = (start_x, start_y + size)
        return (p1, p2, p3, p4, p5, p6)


    def _calculate_adjacency(self, row, column):
        adjacent_hexes = []

        if row <= 4:
            adjacent_hexes.append([row - 1, column - 1])  # NW adjacency top half
            adjacent_hexes.append([row - 1, column])  # NE adjacency top half
        else:
            adjacent_hexes.append([row - 1, column])       # NW adjacency bottom half
            adjacent_hexes.append([row - 1, column + 1])   # NE adjacency bottom half

        adjacent_hexes.append([row, column - 1])      # W adjacency
        adjacent_hexes.append([row, column + 1])      # E adjacency

        if row >= 4:
            adjacent_hexes.append([row + 1, column - 1])  # SW adjacency bottom half
            adjacent_hexes.append([row + 1, column])  # SE adjacency bottom half
        else:
            adjacent_hexes.append([row + 1, column])       # SW adjacency top half
            adjacent_hexes.append([row + 1, column + 1])  # SE adjacency top half

        valid_hexes = []
        for hex in adjacent_hexes:
            row_max = 8
            if hex[0] <= 4:
                col_max = 4 + hex[0]
            else:
                col_max = 4 + (8 - hex[0])

            if hex[0] < 0 or hex[0] > row_max or hex[1] < 0 or hex[1] > col_max:
                continue
            else:
                valid_hexes.append(hex)

        return valid_hexes


    def _coords_to_id(self, coords):
        """Translates 2D coordinates to a Hex ID"""
        row_total = 0
        for row in range(coords[0]):
            row_val = 5 + (4 - abs(4 - row))
            row_total += row_val
        col_val = coords[1] + 1
        return row_total + col_val


    def initialize_start_positions(self, player_data, player_list):
        centre_hex = 31
        self._hexes[centre_hex - 1].set_structure("Refinery", self.create_structure_callback)

        start_positions = [1, 5, 27, 35, 57, 61]
        current_player_index = 0
        for hex in start_positions:
            current_player = player_list[current_player_index]
            self._hexes[hex - 1].change_owner(current_player, current_player.get_colour())
            self._hexes[hex - 1].set_structure("HQ", self.create_structure_callback)
            for adj_hex in self._hexes[hex - 1].get_adjacency_coords():
                adj_id = self._coords_to_id(adj_hex)
                self._hexes[adj_id - 1].change_owner(current_player, current_player.get_colour())

            # current_player.set_hq(hex)
            current_player.set_hq(self._hexes[hex - 1])

            current_player_index += 1


    def create_structure_callback(self, hex, structure):
        if structure == "HQ":
            structure_id = self.hex_grid.create_image(hex.get_structure_coords(), image=self._parent._icon_image_dict["hq"]["map"])
            hex.set_structure_id(structure_id)
        elif structure == "Refinery":
            structure_id = self.hex_grid.create_text(hex.get_structure_coords(), text="@", font=(None, 10))
            hex.set_structure_id(structure_id)


    # def create_squad_icon_callback(self, hex_id, fighter, set_squad_icon_callback):
    #     squad_icon = tk.Label(self, image=self._parent._fighter_image_dict[fighter]["map"], borderwidth=2,
    #                                      relief="ridge", background=self.hex_grid.itemcget(hex_id, "fill"))
    #     starting_slot = self._hexes[hex_id - 1].add_squad(squad_icon)
    #     set_squad_icon_callback(squad_icon, starting_slot)
    #     return

    def create_squad_icon_callback(self, squad):
        squad_hex = squad.get_location()
        squad_icon = tk.Label(self, image=self._parent._fighter_image_dict[squad.get_fighter()]["map"], borderwidth=2,
                              relief="ridge", background=self.hex_grid.itemcget(squad_hex.get_id(), "fill"))
        starting_slot = squad_hex.get_first_open_slot()
        # squad.set_squad_icon(squad_icon, starting_slot)
        squad.set_squad_icon(squad_icon)
        squad_hex.add_squad(squad)
        return


    def get_hex_list(self):
        return self._hexes
