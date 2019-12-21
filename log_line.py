# log_line.py
#
# Defines methods and attributes for a single action log line
# Log types: Move, portal move, attack, combat result, portal attack, pass, build squad, colonize, new turn

REQUIRED_MOVE_ARGUMENTS = ["player_name", "from_hex", "to_hex", "fighter"]
OPTIONAL_MOVE_ARGUMENTS = ["is_vortex"]
ATTACK_ARGUMENTS = ["atk_player", "def_player", "fighter", "from_hex", "to_hex"]
COMBAT_ARGUMENTS = ["atk_player", "def_player", "atk_fighter", "def_fighter", "victor", "hex_id"]
PASS_ARGUMENTS = ["player_name", "fighter", "hex_id"]
BUILD_SQUAD_ARGUMENTS = ["player_name", "fighter", "hex_id", "structure", "is_random"]
COLONIZE_ARGUMENTS = ["player_name", "hex_id", "fighter"]
NEW_TURN_ARGUMENTS = ["turn_num"]


class LogLine:
    def __init__(self, log_type, **kwargs):
        LogLine.validate_log_arguments(log_type, kwargs)
        self._log_type = log_type
        self._kwargs = kwargs

        self._populate_defaults()

    def get_text_log(self):
        kw = self._kwargs
        if self._log_type == "move":
            log_text = LogLine.get_move_text(kw)
            return log_text
        if self._log_type == "attack":
            log_text = LogLine.get_attack_text(kw)
            return log_text
        elif self._log_type == "combat":
            log_text = LogLine.get_combat_text(kw)
            return log_text
        elif self._log_type == "pass":
            log_text = LogLine.get_pass_text(kw)
            return log_text
        elif self._log_type == "build":
            log_text = LogLine.get_build_squad_text(kw)
            return log_text
        elif self._log_type == "colonize":
            log_text = LogLine.get_colonize_text(kw)
            return log_text
        elif self._log_type == "new_turn":
            log_text = LogLine.get_new_turn_text(kw)
            return log_text
        else:
            raise Exception("_log_type is invalid. Ensure log_type argument is being properly validated")

    def _populate_defaults(self):
        if self._log_type == "move":
            if "is_vortex" not in self._kwargs:
                self._kwargs["is_vortex"] = False
            if "is_attack" not in self._kwargs:
                self._kwargs["is_attack"] = False
        if self._log_type == "build":
            if "is_random" not in self._kwargs:
                self._kwargs["random"] = False

    @staticmethod
    def get_move_text(kw):
        template = "{} moved {} from Hex {} to Hex {}"
        formatted_text = template.format(kw["player_name"], kw["fighter"], kw["from_hex"], kw["to_hex"])
        return formatted_text

    @staticmethod
    def get_attack_text(kw):
        template = "{} moved {} from Hex {} to attack {} in Hex {}!"
        formatted_text = template.format(kw["atk_player"], kw["fighter"], kw["from_hex"], kw["def_player"],
                                         kw["to_hex"])
        return formatted_text

    @staticmethod
    def get_combat_text(kw):
        if kw["victor"] == kw["atk_player"]:
            template = "{0}({1}) defeated {2}({3}) in Hex {4}"
        elif kw["victor"] == kw["def_player"]:
            template = "{2}({3}) defended an attack from {0}({1}) in Hex {4}"
        formatted_text = template.format(kw["atk_player"], kw["atk_fighter"], kw["def_player"], kw["def_fighter"], kw["hex_id"])
        return formatted_text

    @staticmethod
    def get_pass_text(kw):
        template = "{} passed with {} in Hex {}"
        formatted_text = template.format(kw["player_name"], kw["fighter"], kw["hex_id"])
        return formatted_text

    @staticmethod
    def get_build_squad_text(kw):
        random_str = " "
        if kw["is_random"] is True:
            random_str = " random "
        template = "{} built a new{}squad at their {} in Hex {}: {}"
        formatted_text = template.format(kw["player_name"], random_str, kw["structure"], kw["hex_id"], kw["fighter"])
        return formatted_text

    @staticmethod
    def get_colonize_text(kw):
        template = "{} colonized Hex {} with {}"
        formatted_text = template.format(kw["player_name"], kw["hex_id"], kw["fighter"])
        return formatted_text

    @staticmethod
    def get_new_turn_text(kw):
        template = "Start of turn {}..."
        formatted_text = template.format(kw["turn_num"])
        return formatted_text

    @staticmethod
    def validate_log_arguments(log_type, kwargs):
        if log_type == "move":
            for arg in kwargs:
                if arg not in REQUIRED_MOVE_ARGUMENTS and arg not in OPTIONAL_MOVE_ARGUMENTS:
                    raise ValueError(arg, "is not a valid option for log type 'move'. Valid args:\n"
                                          "  player_name: str\n"
                                          "  from_hex: int\n"
                                          "  to_hex: int\n"
                                          "  fighter: str\n"
                                          "  is_vortex: bool\n"
                                          "  is_attack: bool")
        elif log_type == "combat":
            pass
        elif log_type == "pass":
            pass
        elif log_type == "build":
            pass
        elif log_type == "colonize":
            pass
        elif log_type == "new_turn":
            pass
        else:
            raise ValueError("Invalid argument for ''log_type''. Valid arguments: move, combat, pass, build, colonize, new_turn")
