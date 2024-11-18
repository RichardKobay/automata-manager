# dfa.py

from models.automata_base import AutomatonBase

class DFA(AutomatonBase):
    """
    Deterministic Finite Automaton (DFA) model.
    """

    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        """
        Initializes a DFA, ensuring deterministic transitions.
        """
        super().__init__(states, alphabet, transitions, start_state, accept_states)
        self._validate_dfa()

    def _validate_dfa(self):
        """
        Ensures that the DFA has deterministic transitions.
        """
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                if len(next_states) > 1:
                    raise ValueError(f"DFA transitions must be deterministic. "
                                    f"State '{state}' with symbol '{symbol}' has multiple transitions.")

    def validate_string(self, input_string: str) -> bool:
        """
        Validates whether the DFA accepts the given input string.

        :param input_string: The input string to validate.
        :return: True if the string is accepted, False otherwise.
        """
        current_state = self.start_state

        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '{symbol}' not in DFA alphabet.")
            if symbol not in self.transitions[current_state]:
                return False  # No transition for the symbol
            next_states = self.transitions[current_state][symbol]
            current_state = next(iter(next_states))  # Move to the next state

        return current_state in self.accept_states
