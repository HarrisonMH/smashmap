# map_app.py
#
# Central map thing
#
# Author: Matt Harrison


import tkinter as tk
import math
import os
from hex_map import HexMap
from hex_menu import HexMenu
from start_menu import StartMenu
from bottom_menu import BottomMenu
from player import Player
from player_menu import PlayerMenu
from PIL import Image, ImageTk, ImageOps

COS_30 = math.cos(math.radians(30))
SIN_30 = math.sin(math.radians(30))
FIGHTER_ICON_PATH = "./images/fighter_icons"
MAP_ICON_PATH = "./images/map_icons"

class MainWindow(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self._master = master

        self._fighter_list = self._generate_fighter_list()
        self._fighter_image_dict = self._generate_fighter_images(self._fighter_list)
        self._icon_image_dict = self._generate_icons()
        self._in_progress = False
        self._players = []
        self._active_menu = "start"

        self._create_widgets(master)


    def _create_widgets(self, master):
        self._hex_map = HexMap(master, self, 50, self._hex_menu_callback)
        self._hex_map.grid(column=0, row=0, columnspan=10, rowspan = 20)
        self.side_menu = StartMenu(master, self._fighter_list, self._start_game_callback)
        self.side_menu.grid(column=11, row=0)


    def _hex_menu_callback(self, hex):
        if self._in_progress == True:
            self.side_menu.grid_forget()
            self.side_menu = HexMenu(hex, self._hex_map, self._fighter_image_dict)
            self.side_menu.grid(column=11, row=0)
            self._active_menu = "hex"


    def _start_game_callback(self, player_data):
        self._initialize_players(player_data)
        self._hex_map.initialize_start_positions(player_data, self._players)
        self._in_progress = True
        self.side_menu.grid_forget()

        # self._hex_map.grid(column=0, row=0, columnspan=10, rowspan=20)

        # self.bottom_menu = BottomMenu(self._master, player_data, self._player_menu_callback)
        self.bottom_menu = BottomMenu(self._master, self._players, self._player_menu_callback, self.end_turn_callback)
        self.bottom_menu.grid(column=0, row=21, pady=5)


    def _player_menu_callback(self, player):
        # player_num = int(event.widget.cget("text")[7])
        print("Opening Player " + str(player.get_player_number()) + " menu")

        self.side_menu.grid_forget()
        self.side_menu = PlayerMenu(self._master, player, self._fighter_image_dict, self._hex_map)
        self.side_menu.grid(column=11, row=0)
        self._active_menu = "player"


    def _battle_popup_callback(self, atk_squad, target_hex):
        self._battle_alert = tk.Toplevel(self, borderwidth=4, relief="raised")
        self._battle_alert.title("BATTLE!")
        self._battle_alert.geometry("+400+300")
        self._battle_alert.resizable(False, False)
        # self._battle_alert.overrideredirect(True)

        attacker = atk_squad.get_owner()
        defender = target_hex.get_squads()[0].get_owner()
        current_row = 0
        header_string = "BATTLE IN HEX " + str(target_hex.get_id()) + "!"
        self._heading = tk.Label(self._battle_alert, text=header_string, font=(None, 20, "bold"))
        self._heading.grid(row=current_row, column=0, columnspan=6)
        current_row += 1
        self._atk_header = tk.Label(self._battle_alert, text="ATTACKER", font=(None, 16))
        self._atk_header.grid(row=current_row, column=0, columnspan=2)
        self._def_header = tk.Label(self._battle_alert, text="DEFENDER", font=(None, 16))
        self._def_header.grid(row=current_row, column=4, columnspan=2)
        current_row += 1

        self._atk_name = tk.Label(self._battle_alert, text=attacker.get_name(), width=15, font=(None, 16), bg=attacker.get_colour(), borderwidth=3, relief="solid")
        self._atk_name.grid(row=current_row, column=0, columnspan=2, padx=5, pady=5)
        self._def_name = tk.Label(self._battle_alert, text=defender.get_name(), width=15, font=(None, 16), bg=defender.get_colour(), borderwidth=3, relief="solid")
        self._def_name.grid(row=current_row, column=4, columnspan=2, padx=5, pady=5)
        current_row += 1

        if len(target_hex.get_squads()) == 1:
            def_col_width = 2
        else:
            def_col_width = 1
            self._def_select_label = tk.Label(self._battle_alert, text="Select Defending Squad:", font=(None, 12, "bold"))
            self._def_select_label.grid(row=current_row, column=4, columnspan=2)
            current_row += 1

        attacker_image = self._fighter_image_dict[atk_squad.get_fighter()]["battle"]
        self._attacker_icon = tk.Label(self._battle_alert, image=attacker_image)
        self._attacker_icon.grid(row=current_row, column=1, padx=5)
        self._vs_label = tk.Label(self._battle_alert, text="VS.", font=(None, 40))
        self._vs_label.grid(row=current_row, column=2, columnspan=2, padx=5, pady=10)
        current_col = 4

        self._def_squads_icons = []

        # if len(target_hex.get_squads()) == 1:
        #     def_col_width = 2
        # else:
        #     def_col_width = 1
        #     self._def_select_label = tk.Label(self._battle_alert, text="Select Defending Squad:", font=(None, 12))
        #     self._def_select_label.grid(row=current_row, column=4, columnspan=2)
        #     current_row += 1

        for def_squad in target_hex.get_squads():
            def_squad_image = self._fighter_image_dict[def_squad.get_fighter()]["battle"]
            if len(target_hex.get_squads()) == 2:
                self._def_squads_icons.append(tk.Button(self._battle_alert, image=def_squad_image, borderwidth=3))
            else:
                self._def_squads_icons.append(tk.Label(self._battle_alert, image=def_squad_image))
            self._def_squads_icons[-1].grid(row=current_row, column=current_col, columnspan=def_col_width, padx=5, pady=10)

            current_col += 1

        current_col = 0




    def _generate_fighter_list(self):
        fighter_list = []
        f = open("fighters.txt")
        fighter_list_raw = f.readlines()
        for fighter in fighter_list_raw:
            fighter_list.append(fighter.rstrip())
        return fighter_list


    def _generate_fighter_images(self, fighter_list):
        fighter_image_dict = {}
        filename_list = []
        for filename in os.listdir(FIGHTER_ICON_PATH):
            filename_list.append(filename)
            print(filename)

        print(len(filename_list))
        f_index = 0
        for fighter in fighter_list:
            # print(fighter, f_index)
            raw_image = Image.open(FIGHTER_ICON_PATH + "/" + filename_list[f_index])
            menu_image = raw_image.resize((50, 50))
            map_image_normal = raw_image.resize((30, 30))
            map_image_bw = ImageOps.grayscale(map_image_normal)
            battle_image_object = ImageTk.PhotoImage(raw_image)
            menu_image_object = ImageTk.PhotoImage(menu_image)
            map_image_normal_object = ImageTk.PhotoImage(map_image_normal)
            map_image_bw_object = ImageTk.PhotoImage(map_image_bw)
            fighter_image_dict[fighter] = {}
            fighter_image_dict[fighter]["battle"] = battle_image_object
            fighter_image_dict[fighter]["menu"] = menu_image_object
            fighter_image_dict[fighter]["map"] = map_image_normal_object
            fighter_image_dict[fighter]["map_bw"] = map_image_bw_object
            f_index += 1
        # print(fighter_image_dict)
        return fighter_image_dict


    def _generate_icons(self):
        icon_dict = {}
        filename_list = []
        for filename in os.listdir(MAP_ICON_PATH):
            filename_list.append(filename)
        for icon_file in filename_list:
            filename_root = icon_file.split('.')[0]
            raw_image = Image.open(MAP_ICON_PATH + "/" + icon_file).convert("RGBA")
            menu_image = raw_image.resize((50, 50))
            map_image_normal = raw_image.resize((25, 25))
            menu_image_object = ImageTk.PhotoImage(menu_image)
            map_image_normal_object = ImageTk.PhotoImage(map_image_normal)
            icon_dict[filename_root] = {}
            icon_dict[filename_root]["menu"] = menu_image_object
            icon_dict[filename_root]["map"] = map_image_normal_object
        return icon_dict


    def _initialize_players(self, player_data):
        for player in player_data:
            self._players.append(Player(self._master, player_data[player], self._hex_map.create_squad_icon_callback, self._player_menu_callback, self._hex_menu_callback, self._battle_popup_callback))


    def get_active_menu(self):
        return self._active_menu


    def end_turn_callback(self):
        for player in self._players:
            for squad in player.get_squads():
                squad.refresh_turn()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Smash Map Ladder v0.1")
    root.geometry("+100+100")
    root.resizable(False, False)
    app = MainWindow(root)
    app.mainloop()