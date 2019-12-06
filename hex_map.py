# hex_map.py
#
#
#
#

import tkinter as tk
import math
from hex import Hex
from squad_context_menu import SquadContextMenu

COS_30 = math.cos(math.radians(30))
SIN_30 = math.sin(math.radians(30))
TEST_WIDTH_50 = COS_30 * 100


class HexMap(tk.Frame):

    def __init__(self, master, parent, size, hex_menu_callback, end_turn_callback, next_player_callback):
        super().__init__(master)
        self._master = master
        self._parent = parent
        self.hex_grid = tk.Canvas(self, height=780, width=900, bg="white")
        self.hex_grid.grid(column=0, row=1)
        self._hex_menu_callback = hex_menu_callback
        self._end_turn_callback = end_turn_callback
        self._next_player_callback = next_player_callback

        self._hex_coord_dict = {}
        self._hexes = []

        self._create_grid(size)
        # self._create_squad_slots()
        self._define_squad_slot_coords()
        self._create_structure_slots()
        self._label_grid()
        self._map_menu = tk.Frame()
        self._create_master_menu()


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

    def _create_master_menu(self):
        current_row = 0
        self._turn_num_label = tk.Label(self._map_menu, text="Turn " + str(self._parent.get_turn_number()),
                                        font=(None, 12, "bold"))
        self._turn_num_label.grid(row=current_row, column=0, columnspan=2)
        current_row += 1
        self._current_player_label_1 = tk.Label(self._map_menu, text="Current Player:", font=(None, 10, "bold"))
        self._current_player_label_1.grid(row=current_row, column=0, sticky="W")
        self._current_player_label_2 = tk.Label(self._map_menu, fg="white", font=(None, 10, "bold"))
        self._current_player_label_2.grid(row=current_row, column=1, sticky="W")
        current_row += 1
        self._next_player_btn = tk.Button(self._map_menu, text="Next Player", command=self._next_player_callback)
        self._next_player_btn.grid(row=current_row, column=0, columnspan=2, sticky="W"+"E")
        current_row += 1
        self._end_turn_btn = tk.Button(self._map_menu, text="End Turn", command=self._end_turn_callback)
        self._end_turn_btn.grid(row=current_row, column=0, columnspan=2, sticky="W" + "E")

        self._grid_menu_window = self.hex_grid.create_window(0, 0, anchor="nw", window=self._map_menu)

    def adjust_current_player_display(self, value):
        current_player = value
        self._current_player_label_2.config(text=current_player.get_name(), bg=current_player.get_colour())

    def adjust_turn_display(self, value):
        self._turn_num_label.config(text="Turn " + str(value))

    def _create_hex(self, start_x, start_y, size, row, column):
        hex_points = self._calculate_hex_points(start_x, start_y, size)
        hex_id = self.hex_grid.create_polygon(hex_points[0][0], hex_points[0][1], hex_points[1][0], hex_points[1][1],
                                              hex_points[2][0], hex_points[2][1], hex_points[3][0], hex_points[3][1],
                                              hex_points[4][0], hex_points[4][1], hex_points[5][0], hex_points[5][1],
                                              fill="white", outline="black", activedash=True, width=2)
        self._hex_coord_dict[hex_id] = hex_points
        adjacent_hexes = self._calculate_adjacency(row, column)
        ring_number = self.find_ring_number((row, column))
        # structure = "None"
        # if hex_id == 31:
        #     structure = "Refinery"
        self._hexes.append(Hex(self.hex_grid, self._master, self, hex_id, self._hex_menu_callback, row, column, adjacent_hexes, ring_number, self._parent.get_selected_squad))
        self.hex_grid.tag_bind(hex_id, "<Button-3>", self._hexes[-1].hex_right_click)
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

    def find_ring_number(self, grid_coords):
        row = grid_coords[0]
        col = grid_coords[1]
        if row == 0 or row == 8:
            return 1
        elif row == 1 or row == 7:
            col_max = 5
        elif row == 2 or row == 6:
            col_max = 6
        elif row == 3 or row == 5:
            col_max = 7
        elif row == 4:
            col_max = 8

        if col == 0 or col == col_max:
            return 1
        if col == 1 or col == col_max - 1:
            return 2
        if col == 2 or col == col_max - 2:
            return 3
        if col == 3 or col == col_max - 3:
            return 4
        if col == 4 and col == col_max - 4:
            return 5


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

        factory_positions = [15, 21, 24, 38, 41, 47]
        for hex in factory_positions:
            self._hexes[hex - 1].set_structure("Factory", self.create_structure_callback)

        mine_positions = [3, 12, 18, 44, 50, 59, 22, 23, 30, 32, 39, 40]
        for hex in mine_positions:
            self._hexes[hex - 1].set_structure("Mine", self.create_structure_callback)

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
            hex.set_value(175)
        elif structure == "Refinery":
            structure_id = self.hex_grid.create_text(hex.get_structure_coords(), text="@", font=(None, 10))
            hex.set_structure_id(structure_id)
            hex.set_value(200)
        elif structure == "Factory":
            structure_id = self.hex_grid.create_image(hex.get_structure_coords(),
                                                      image=self._parent._icon_image_dict["factory"]["map"])
            hex.set_structure_id(structure_id)
        elif structure == "Mine":
            structure_id = self.hex_grid.create_image(hex.get_structure_coords(),
                                                      image=self._parent._icon_image_dict["mine"]["map"])
            hex.set_structure_id(structure_id)
            hex.set_value(50)

    def create_squad_icon_callback(self, squad):
        squad_hex = squad.get_location()
        squad_icon = tk.Label(self, image=self._parent._fighter_image_dict[squad.get_fighter()]["map"], borderwidth=2,
                              relief="ridge", background=self.hex_grid.itemcget(squad_hex.get_id(), "fill"))
        # starting_slot = squad_hex.get_first_open_slot()
        # squad.set_squad_icon(squad_icon, starting_slot)
        squad.set_squad_icon(squad_icon)
        squad_hex.add_squad(squad)
        return

    def get_hex_list(self):
        return self._hexes

    def _squad_context_menu_callback(self, squad):
        squad_coords = self.hex_grid.coords(squad.get_squad_slot_id())
        canvas_item_id = self.hex_grid.create_window(squad_coords[0] + 15, squad_coords[1], anchor="w")
        self._squad_context_menu = SquadContextMenu(self, squad, canvas_item_id, self._destroy_squad_context_menu_callback)
        self.hex_grid.itemconfig(canvas_item_id, window=self._squad_context_menu)
        self.hex_grid.tag_bind(canvas_item_id, "<Leave>", self._squad_context_menu.mouse_exit)

    def _destroy_squad_context_menu_callback(self, canvas_item_id):
        self.hex_grid.delete(canvas_item_id)