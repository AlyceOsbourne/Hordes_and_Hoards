"""
Dungeon Module for Hordes and Hoards, handles the generation of dungeons to be used in the game.
"""
from pygame_core import get_handles
event_handler, asset_manager, state_manager = get_handles()


# REGISTER EVENTS

def register_events():
    """
    Register events for the dungeon module.
    :return: NoneType
    """
    dungeon_events = [event_handler.create_event_type(name) for name in [
        "START_DUNGEON_GENERATION",
        "DUNGEON_GENERATION_COMPLETE",
        "START_DUNGEON",
        "PLAYER_MOVE",
        "PLAYER_ATTACK",
        "PLAYER_DAMAGE",
        "PLAYER_DEATH",
        "MINION_MOVE",
        "MINION_ATTACK",
        "MINION_DAMAGE",
        "MINION_DEATH",
        "ADVENTURER_MOVE",
        "ADVENTURER_ATTACK",
        "ADVENTURER_DAMAGE",
        "ADVENTURER_DEATH",
        "ADVENTURER_GRAB_LOOT",
        "ADVENTURER_DROP_LOOT"

    ]]

    print(f"registered {len(dungeon_events)} dungeon events")

# REGISTER STATES

def register_states():
    """
    Register states for the dungeon module.
    :return: NoneType
    """
    states = {
        # todo add states
    }
    print("registering states...")
    for state, default in states:
        state_manager.register_state(state, default)
    print(f"registered {len(states)} states")


class Test:
    """some test class"""

    def some_func(self):
        """
        some funct doc
        :return:
        """