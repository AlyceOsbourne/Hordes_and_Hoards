class StateHandler:
    """This is the object we will save and load from disk to act as the save game, maybe?"""

    def __init__(self):
        print("Initializing game state handler...")
        self.states = {}

        print("Game state handler initialized.")

    # we are using raises to make sure all things are being registered and accessed properly,
    # this is an attempt to make sure some types of bugs are mitigated, and not just ignored

    # The following two functions are basically the same, but with intent,
    # this is mostly for readability, and to make sure I ah thinking about the flow of code
    def add_state(self, state_name: str, default_state):
        if state_name in self.states:
            raise KeyError(f"State with name {state_name} already exists.")
        self.states[state_name] = default_state

    def add_states(self, **states):
        for state_name, state in states.items():
            self.add_state(state_name, state)

    def set_state(self, state_name: str, state):
        if state_name not in self.states:
            raise KeyError(f"State with name {state_name} does not exist.")
        self.states[state_name] = state

    def set_states(self, **states):
        for state_name, state in states.items():
            self.set_state(state_name, state)

    def remove_state(self, state_name: str):
        if state_name not in self.states:
            raise KeyError(f"State with name {state_name} does not exist.")
        del self.states[state_name]

    def remove_states(self, *state_names):
        for state_name in state_names:
            self.remove_state(state_name)

    def get_state(self, state_name: str):
        if state_name not in self.states:
            raise KeyError(f"State with name {state_name} does not exist.")
        return self.states[state_name]

    def get_states(self, *state_names):
        return [self.get_state(state_name) for state_name in state_names]

    def get_all_states(self):
        return self.states

    def has_state(self, state_name: str):
        return state_name in self.states

