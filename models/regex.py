# regex.py

from typing import Any
from nfa_e import NFAE

class RegularExpression:
    """
    Regular Expression model with utilities for conversion to finite automata.
    """

    def __init__(self, pattern: str):
        """
        Initializes a Regular Expression.

        :param pattern: The string pattern representing the regular expression.
        """
        self.pattern = pattern
        self._validate_pattern()

    def _validate_pattern(self):
        """
        Validates the syntax of the regular expression.
        """
        # A basic validation for demonstration. Expand as needed.
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789|*+?().")
        for char in self.pattern:
            if char not in valid_chars:
                raise ValueError(f"Invalid character '{char}' in regular expression.")
        if not self.pattern:
            raise ValueError("Regular expression cannot be empty.")

    def _thompson_construct(self, sub_pattern: str) -> NFAE:
        """
        Recursively constructs an NFA-e for a given sub-pattern using Thompson's algorithm.

        :param sub_pattern: A part of the regular expression.
        :return: An instance of NFAE for the sub-pattern.
        """
        from itertools import count
        unique_id = count()  # Generator for unique state IDs

        def new_state():
            return f"q{next(unique_id)}"

        stack = []

        for char in sub_pattern:
            if char.isalnum():  # Single character
                start = new_state()
                end = new_state()
                transitions = {start: {char: {end}}}
                stack.append(NFAE(
                    states={start, end},
                    alphabet={char},
                    transitions=transitions,
                    start_state=start,
                    accept_states={end}
                ))
            elif char == '*':  # Kleene star
                nfa = stack.pop()
                start = new_state()
                end = new_state()
                transitions = {
                    start: {'ε': {nfa.start_state, end}},
                    **nfa.transitions,
                    list(nfa.accept_states)[0]: {'ε': {nfa.start_state, end}}
                }
                stack.append(NFAE(
                    states={start, end, *nfa.states},
                    alphabet=nfa.alphabet,
                    transitions=transitions,
                    start_state=start,
                    accept_states={end}
                ))
            elif char == '|':  # Union
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                start = new_state()
                end = new_state()
                transitions = {
                    start: {'ε': {nfa1.start_state, nfa2.start_state}},
                    **nfa1.transitions,
                    **nfa2.transitions,
                    list(nfa1.accept_states)[0]: {'ε': {end}},
                    list(nfa2.accept_states)[0]: {'ε': {end}}
                }
                stack.append(NFAE(
                    states={start, end, *nfa1.states, *nfa2.states},
                    alphabet=nfa1.alphabet | nfa2.alphabet,
                    transitions=transitions,
                    start_state=start,
                    accept_states={end}
                ))
            elif char == '.':  # Concatenation
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                transitions = {
                    **nfa1.transitions,
                    **nfa2.transitions,
                    list(nfa1.accept_states)[0]: {'ε': {nfa2.start_state}}
                }
                stack.append(NFAE(
                    states=nfa1.states | nfa2.states,
                    alphabet=nfa1.alphabet | nfa2.alphabet,
                    transitions=transitions,
                    start_state=nfa1.start_state,
                    accept_states=nfa2.accept_states
                ))

        if len(stack) != 1:
            raise ValueError("Invalid regular expression pattern.")

        return stack.pop()

    def to_nfa_e(self) -> NFAE:
        """
        Converts the regular expression to an NFA-e.
        (Uses Thompson's construction algorithm.)

        :return: An instance of NFAE representing the regular expression.
        """
        return self._thompson_construct(self.pattern)

    def to_dfa(self) -> Any:
        """
        Converts the regular expression to a DFA.
        (This would typically first convert to an NFA-e and then to a DFA.)

        :return: An instance of DFA representing the regular expression.
        """
        nfa_e = self.to_nfa_e()
        return nfa_e.to_dfa()  # Assumes NFAE has a method to convert to DFA

    def __str__(self) -> str:
        """
        Returns a string representation of the regular expression.
        """
        return self.pattern
