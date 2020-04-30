# map_app.py
#
# Central map thing
#
# Author: Matt Harrison


import tkinter as tk
import math
import os
import json
from hex_map import HexMap
from start_menu import StartMenu
from bottom_menu import BottomMenu
from player import Player
from battle_popup import BattlePopup
from end_turn_popup import EndTurnPopup
from side_menu import SideMenu
from play_log import PlayLog
from battle_in_progress import BattleInProgress

from PIL import Image, ImageTk, ImageOps

COS_30 = math.cos(math.radians(30))
SIN_30 = math.sin(math.radians(30))
FIGHTER_ICON_PATH = "./images/fighter_icons"
MAP_ICON_PATH = "./images/map_icons"
SAVE_FILE_PATH = "./saves"


class MainWindow(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master, bg="white")
        self._master = master
        self._fighter_list = self._generate_fighter_list()
        self._fighter_image_dict = self._generate_fighter_images(self._fighter_list)
        self._icon_image_dict = self._generate_icons()
        self._in_progress = False
        self._players = []
        self._active_menu = "start"
        self._turn_number = 1
        self._selected_squad = None
        self._current_player_index = 0

        self._create_widgets(master)

    def _create_widgets(self, master):
        self._hex_map = HexMap(master, self, 50, self._side_menu_callback, self._end_turn_callback, self.next_player)
        self._start_menu = StartMenu(master, self._fighter_list, self._start_game_callback, self._load_game_callback)
        self._start_menu.grid(column=0, row=0)
        self._status_menu = tk.Frame(master, width=500, height=20, background="white")
        self._play_log = PlayLog(self._status_menu, background="white")
        self._play_log.pack()

    # def _hex_menu_callback(self, hex):
    #     print("Hex menu callback, hex", hex.get_id())
    #     if self._in_progress:
    #         if self._side_menu is not None:
    #             self._side_menu.grid_forget()
    #         self._side_menu = HexMenu(hex, self._hex_map, self._fighter_image_dict, self._fighter_list)
    #         self._side_menu.grid(column=11, row=0)
    #         self._active_menu = "hex"

    def _side_menu_callback(self, hex):
        if self._in_progress:
            if self._side_menu is not None:
                self._side_menu.update_all(hex)


    def _start_game_callback(self, player_data):
        self._hex_map.grid(column=1, row=0)
        self._initialize_players(player_data)
        self._hex_map.initialize_structures()
        self._hex_map.initialize_start_locations(self._players)
        self._hex_map.adjust_current_player_display(self._players[0])
        self._in_progress = True
        self._start_menu.destroy()
        self._side_menu = SideMenu(self._master, self, self._players[0].get_hq(), self._hex_map,
                                   self._fighter_image_dict, self._fighter_list, self._icon_image_dict)
        self._side_menu.grid(column=2, row=0, rowspan=2, sticky="n")
        self.bottom_menu = BottomMenu(self._master, self._players, self._end_turn_callback, self._icon_image_dict)
        self.bottom_menu.grid(column=1, row=1, pady=5)
        self._status_menu.grid(column=0, row=0, rowspan=2, sticky="nw")
        self._play_log.create_new_log("new_turn", turn_num=self._turn_number)


    def _load_game_callback(self, filename=None):
        if filename is None:
            save_file_path = SAVE_FILE_PATH + "/savedata.txt"
        else:
            save_file_path = SAVE_FILE_PATH + "/" + filename
        f = open(save_file_path)
        data_text = f.read()
        data_dict = json.loads(data_text)

        self._hex_map.initialize_structures()
        hex_list = self._hex_map.get_hex_list()
        for player_data in data_dict["players"]:
            self._players.append(Player(self, player_data, self._hex_map, self._hex_map.create_squad_icon_callback,
                                        self._side_menu_callback, self._battle_popup_callback, self.get_current_player, True))
            print("Setting HQ for", self._players[-1].get_name(), ": Hex", hex_list[player_data["hq_id"] - 1].get_id())
            self._players[-1].set_hq(hex_list[player_data["hq_id"] - 1])
            print("")
            self._players[-1].set_resources(player_data["resources"])
            self._players[-1].set_income(player_data["income"])
            self._players[-1].set_territory_size(player_data["territory_size"])
            self._players[-1].set_vp(player_data["vp"])
            self._players[-1].set_vp_income(player_data["vp_income"])
            for squad in player_data["squads"]:
                self._players[-1].load_squad(squad)

        for hex in data_dict["hexes"]:
            for player in self._players:
                # print("Hex owner:", type(hex["owner"]), "Player:", type(player.get_player_number()))
                if hex["owner"] == player.get_player_number():
                    print("Updating owner of hex", hex["id"])
                    hex_list[hex["id"] - 1].change_owner(player, player.get_colour())
                    break

        self._turn_number = data_dict["game"]["turn"]
        self._current_player_index = data_dict["game"]["current_player"]
        self._current_player = self._players[self._current_player_index]
        self._hex_map.adjust_current_player_display(self._current_player)
        self._hex_map.adjust_turn_display(self._turn_number)

        self._in_progress = True
        self._start_menu.destroy()
        self._hex_map.grid(column=1, row=0)

        self._side_menu = SideMenu(self._master, self, self._players[0].get_hq(), self._hex_map,
                                   self._fighter_image_dict, self._fighter_list, self._icon_image_dict)
        self._side_menu.grid(column=2, row=0, rowspan=2, sticky="n")
        self.bottom_menu = BottomMenu(self._master, self._players, self._end_turn_callback, self._icon_image_dict)
        self.bottom_menu.grid(column=1, row=1, pady=5)
        self._status_menu.grid(column=0, row=0, rowspan=2, sticky="nw")


    def _battle_popup_callback(self, atk_squad, target_hex):
        self._battle_popup = BattlePopup(self, atk_squad, target_hex, self._fighter_image_dict,
                                         self._close_battle_popup_callback, self._hex_map)


    def _close_battle_popup_callback(self):
        self._battle_popup.destroy()

    def _generate_fighter_list(self):
        fighter_list = ["Random"]
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
            if fighter == "Random":
                continue
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
            self._players.append(Player(self, player_data[player], self._hex_map, self._hex_map.create_squad_icon_callback,
                                        self._side_menu_callback, self._battle_popup_callback, self.get_current_player))

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
                    if player_sorted.get_vp() <= player.get_vp() < sorted_list[i + 1].get_vp():
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

    # def _next_player_callback(self):
    #     if self._current_player_index < len(self._players) - 1:
    #         self._current_player_index += 1
    #     else:
    #         self._current_player_index = 0
    #         self.end_turn()
    #     self._hex_map.adjust_current_player_display(self.get_current_player())

    def next_player(self, pass_count=0):
        # Revised to rotate after each action
        if self._current_player_index < len(self._players) - 1:
            self._current_player_index += 1
        else:
            self._current_player_index = 0
        if pass_count == len(self._players):
            self.end_turn()
        if self.get_current_player().check_remaining_actions() is False:
            self.next_player(pass_count + 1)

        self._hex_map.adjust_current_player_display(self.get_current_player())

    def end_turn(self):
        self._turn_number += 1
        self._hex_map.adjust_turn_display(self._turn_number)
        for player in self._players:
            player.collect_income()
            player.collect_vp()
            player.refresh_player_squads()
        self._players = self.sort_players_by_vp()
        self.bottom_menu.refresh_widget_order(self._players)
        self._play_log.create_new_log("new_turn", turn_num=self._turn_number)

    def get_current_player(self):
        # print("Current player index: ", self._current_player_index)
        return self._players[self._current_player_index]

    def get_fighter_list(self):
        return self._fighter_list

    def save_state_as_json(self):
        # Players - > Squads -> Hexes
        data_dict = {
            "game": {
                "turn": self._turn_number,
                "current_player": self._current_player_index
            },
            "players": [],
            "hexes": []
        }
        for player in self._players:
            player_dict = {
                "playernum": str(player.get_player_number()),
                "name": player.get_name(),
                "colour": player.get_colour(),
                "hq_id": player.get_hq().get_id(),
                "resources": player.get_resources(),
                "income": player.get_income(),
                "basecost": player.get_base_squad_cost(),
                "forcerandom": player.get_force_random(),
                "territory_size": player.get_territory_size(),
                "vp": player.get_vp(),
                "vp_income": player.get_vp_income(),
                "squads": []
            }
            for squad in player.get_squads():
                squad_dict = {
                    "fighter": squad.get_fighter(),
                    "kills": squad.get_kills(),
                    "bounty": squad.get_bounty(),
                    "location": squad.get_location().get_id(),
                    "turn_taken": squad.get_turn_status()
                }
                player_dict["squads"].append(squad_dict)
            data_dict["players"].append(player_dict)

        for hex in self._hex_map.get_hex_list():
            if hex.get_owner() is not None:
                hex_dict = {
                    "id": hex.get_id(),
                    "owner": hex.get_owner().get_player_number()
                }
                data_dict["hexes"].append(hex_dict)
        self.save_dict_to_file(data_dict)


    def save_dict_to_file(self, data_dict):
        json_data = json.dumps(data_dict, indent=4)
        if not os.path.exists(SAVE_FILE_PATH):
            os.mkdir(SAVE_FILE_PATH)
        save_file = SAVE_FILE_PATH + "/savedata.txt"
        file = open(save_file, 'w')
        file.write(json_data)
        file.close()

    def get_play_log(self):
        return self._play_log

    def create_bip_callback(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Smash Map Ladder v0.8")
    root.geometry("+100+50")
    root.resizable(False, False)
    app = MainWindow(root)
    app.mainloop()
