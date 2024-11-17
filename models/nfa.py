# nfa.py

from automata_base import AutomatonBase

class NFA(AutomatonBase):
    """
    Nondeterministic Finite Automaton (NFA) model.
    """

    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        """
        Initializes an NFA.
        """
        super().__init__(states, alphabet, transitions, start_state, accept_states)

    def validate_string(self, input_string: str) -> bool:
        """
        Validates whether the NFA accepts the given input string.

        :param input_string: The input string to validate.
        :return: True if the string is accepted, False otherwise.
        """
        current_states = {self.start_state}

        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '{symbol}' not in NFA alphabet.")
            
            next_states = set()
            for state in current_states:
                if symbol in self.transitions.get(state, {}):
                    next_states.update(self.transitions[state][symbol])
            current_states = next_states

        return any(state in self.accept_states for state in current_states)
