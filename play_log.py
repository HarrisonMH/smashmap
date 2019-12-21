# play_log.py
#
# Defines attributes, methods and layout for play log

import tkinter as tk
from log_line import LogLine

DISPLAY_SIZE = 20


# Valid keywords: player1, player2, hex1, hex2, squad1, squad2, turn_num, victor
class PlayLog(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, kwargs)

        self._log_list = []
        self._display_log = []

        self._header = tk.Label(self, text="Play Log")
        self._header.pack()

    def create_new_log(self, log_type, **kwargs):
        if log_type == "move":
            self._log_list.append(PlayLog._create_move_log(log_type, kwargs))
        elif log_type == "attack":
            self._log_list.append(PlayLog._create_attack_log(log_type, kwargs))
        elif log_type == "combat":
            self._log_list.append(PlayLog._create_attack_log(log_type, kwargs))
        elif log_type == "pass":
            self._log_list.append(PlayLog._create_pass_log(log_type, kwargs))
        elif log_type == "build":
            self._log_list.append(PlayLog._create_build_log(log_type, kwargs))
        elif log_type == "colonize":
            self._log_list.append(PlayLog._create_colonize_log(log_type, kwargs))
        elif log_type == "new_turn":
            self._log_list.append(PlayLog._create_new_turn_log(log_type, kwargs))
        print(self._log_list[-1].get_text_log())
        self._display_new_text_log()


    def _display_new_text_log(self):
        log_length = len(self._log_list)
        print("Log count: ", len(self._display_log))
        if len(self._display_log) > DISPLAY_SIZE:
            self._display_log[0].destroy()
            del self._display_log[0]
        self._display_log.append(tk.Label(self, text=self._log_list[-1].get_text_log(), width=40, anchor="w"))
        self._display_log[-1].pack()


    @staticmethod
    def _create_move_log(log_type, kwargs):
        player_name = kwargs["player1"].get_name()
        fighter = kwargs["squad1"].get_fighter()
        from_hex = kwargs["hex1"].get_id()
        to_hex = kwargs["hex2"].get_id()
        new_log_line = LogLine(log_type, player_name=player_name, fighter=fighter, from_hex=from_hex, to_hex=to_hex)
        return new_log_line

    @staticmethod
    def _create_attack_log(log_type, kwargs):
        atk_player = kwargs["player1"].get_name()
        def_player = kwargs["player2"].get_name()
        fighter = kwargs["squad1"].get_fighter()
        from_hex = kwargs["hex1"].get_id()
        to_hex = kwargs["hex2"].get_id()
        new_log_line = LogLine(log_type, atk_player=atk_player, def_player=def_player, fighter=fighter,
                               from_hex=from_hex, to_hex=to_hex)
        return new_log_line

    @staticmethod
    def _create_combat_log(log_type, kwargs):
        atk_player = kwargs["player1"].get_name()
        def_player = kwargs["player2"].get_name()
        atk_fighter = kwargs["squad1"].get_fighter()
        def_fighter = kwargs["squad2"].get_fighter()
        victor = kwargs["victor"].get_name()
        hex_id = kwargs["hex1"].get_id()
        new_log_line = LogLine(log_type, atk_player=atk_player, def_player=def_player, atk_fighter=atk_fighter,
                               def_fighter=def_fighter, victor=victor, hex_id=hex_id)
        return new_log_line

    @staticmethod
    def _create_pass_log(log_type, kwargs):
        player_name = kwargs["player1"].get_name()
        fighter = kwargs["squad1"].get_fighter()
        hex_id = kwargs["hex1"].get_id()
        new_log_line = LogLine(log_type, player_name=player_name, fighter=fighter, hex_id=hex_id)
        return new_log_line

    @staticmethod
    def _create_build_log(log_type, kwargs):
        player_name = kwargs["player1"].get_name()
        fighter = kwargs["squad1"].get_fighter()
        hex_id = kwargs["hex1"].get_id()
        structure = kwargs["hex1"].get_structure()
        # FIXME: Add code to display when squad build is random
        is_random = False
        new_log_line = LogLine(log_type, player_name=player_name, fighter=fighter, hex_id=hex_id, structure=structure,
                               is_random=is_random)
        return new_log_line

    @staticmethod
    def _create_colonize_log(log_type, kwargs):
        player_name = kwargs["player1"].get_name()
        fighter = kwargs["squad1"].get_fighter()
        hex_id = kwargs["hex1"].get_id()
        new_log_line = LogLine(log_type, player_name=player_name, fighter=fighter, hex_id=hex_id)
        return new_log_line

    @staticmethod
    def _create_new_turn_log(log_type, kwargs):
        turn_num = kwargs["turn_num"]
        new_log_line = LogLine(log_type, turn_num=turn_num)
        return new_log_line

    # FIXME: Add argument validation
