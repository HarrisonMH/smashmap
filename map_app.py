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
from battle_popup import BattlePopup
from end_turn_popup import EndTurnPopup
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
        self._turn_number = 1
        self._selected_squad = None

        self._create_widgets(master)

    def _create_widgets(self, master):
        self._hex_map = HexMap(master, self, 50, self._hex_menu_callback, self._end_turn_callback)
        self._hex_map.grid(column=0, row=0, columnspan=6, rowspan=20)
        self.side_menu = StartMenu(master, self._fighter_list, self._start_game_callback)
        self.side_menu.grid(column=11, row=0)

    def _hex_menu_callback(self, hex):
        if self._in_progress:
            self.side_menu.grid_forget()
            self.side_menu = HexMenu(hex, self._hex_map, self._fighter_image_dict, self._fighter_list)
            self.side_menu.grid(column=11, row=0)
            self._active_menu = "hex"


    def _start_game_callback(self, player_data):
        self._initialize_players(player_data)
        self._hex_map.initialize_start_positions(player_data, self._players)
        self._in_progress = True
        self.side_menu.grid_forget()

        # self._hex_map.grid(column=0, row=0, columnspan=10, rowspan=20)

        # self.bottom_menu = BottomMenu(self._master, player_data, self._player_menu_callback)
        self.bottom_menu = BottomMenu(self._master, self._players, self._player_menu_callback, self._end_turn_callback, self._icon_image_dict)
        self.bottom_menu.grid(column=0, row=21, columnspan=6, pady=5)


    def _player_menu_callback(self, player):
        # player_num = int(event.widget.cget("text")[7])
        print("Opening Player " + str(player.get_player_number()) + " menu")

        self.side_menu.grid_forget()
        self.side_menu = PlayerMenu(self._master, player, self._fighter_image_dict, self._hex_map)
        self.side_menu.grid(column=11, row=0)
        self._active_menu = "player"


    def _battle_popup_callback(self, atk_squad, target_hex):
        self._battle_popup = BattlePopup(self, atk_squad, target_hex, self._fighter_image_dict,
                                         self._close_battle_popup_callback, self._hex_map)


    def _close_battle_popup_callback(self):
        self._battle_popup.destroy()

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
            # print(filename)

        print("Generating", len(filename_list), "fighter icons...")
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
            self._players.append(Player(self, player_data[player], self._hex_map.create_squad_icon_callback, self._player_menu_callback, self._hex_menu_callback, self._battle_popup_callback))

    def _select_defending_squad(self):
        pass

    def get_turn_number(self):
        return self._turn_number

    def get_selected_squad(self):
        return self._selected_squad

    def set_selected_squad(self, squad):
        if squad is None:
            self._selected_squad = squad
            return
        elif self._selected_squad is not None:
            self._selected_squad.deselect_squad()
        self._selected_squad = squad
        print("Selected squad: ", self._selected_squad.get_fighter())


    def get_active_menu(self):
        return self._active_menu

    def sort_players_by_vp(self):
        sorted_list = []
        max_value = 0
        for player in self._players:
            if len(sorted_list) == 0:
                sorted_list.append(player)
                max_value = player.get_vp()
            elif player.get_vp() < sorted_list[0].get_vp():
                sorted_list.insert(0, player)
            elif player.get_vp() >= max_value:
                sorted_list.append(player)
                max_value = player.get_vp()
            else:
                for i, player_sorted in enumerate(sorted_list):
                    if player.get_vp() >= player_sorted.get_vp() and player.get_vp() < sorted_list[i+1].get_vp():
                        print(player.get_name(), ": ", player.get_vp(), " is between ", player_sorted.get_name(), ": ", player_sorted.get_vp(), " and ", sorted_list[i+1].get_name(), ": ", sorted_list[i+1].get_vp())
                        sorted_list.insert(i+1, player)
                        break
        print("New turn order:")
        for player in sorted_list:
            print(player.get_name())
        return sorted_list

    def _confirm_end_turn(self, player_list):
        self._end_turn_popup = EndTurnPopup(self, player_list, self._close_confirm_end_turn, self.end_turn)

    def _close_confirm_end_turn(self):
        self._end_turn_popup.destroy()

    def _end_turn_callback(self):
        players_actions_remaining = []
        for player in self._players:
            if player.check_remaining_actions() is True:
                players_actions_remaining.append(player)
        if len(players_actions_remaining) > 0:
            self._confirm_end_turn(players_actions_remaining)
        else:
            self.end_turn()

    def end_turn(self):
        self._turn_number += 1
        self._hex_map.adjust_turn_display(self._turn_number)
        for player in self._players:
            player.collect_income()
            player.collect_vp()
            player.refresh_player_squads()
        sorted_player_list = self.sort_players_by_vp()
        self.bottom_menu.refresh_widget_order(sorted_player_list)




if __name__ == "__main__":
    root = tk.Tk()
    root.title("Smash Map Ladder v0.1")
    root.geometry("+100+50")
    root.resizable(False, False)
    app = MainWindow(root)
    app.mainloop()
