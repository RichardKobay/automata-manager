# nfa_e.py

from automata_base import AutomatonBase
from nfa import NFA
from dfa import DFA

class NFAE(AutomatonBase):
    """
    Nondeterministic Finite Automaton with Epsilon transitions (NFA-e) model.
    """

    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        """
        Initializes an NFA-e.
        """
        super().__init__(states, alphabet, transitions, start_state, accept_states)

    def _epsilon_closure(self, states: set) -> set:
        """
        Computes the epsilon-closure for a set of states.

        :param states: The set of states to compute epsilon-closure for.
        :return: A set of states reachable through epsilon transitions.
        """
        closure = set(states)
        stack = list(states)

        while stack:
            current = stack.pop()
            for next_state in self.transitions.get(current, {}).get('ε', []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure

    def validate_string(self, input_string: str) -> bool:
        """
        Validates whether the NFA-e accepts the given input string.

        :param input_string: The input string to validate.
        :return: True if the string is accepted, False otherwise.
        """
        current_states = self._epsilon_closure({self.start_state})

        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '{symbol}' not in NFA-e alphabet.")
            next_states = set()
            for state in current_states:
                if symbol in self.transitions.get(state, {}):
                    next_states.update(self.transitions[state][symbol])
            current_states = self._epsilon_closure(next_states)

        return any(state in self.accept_states for state in current_states)
    
    def to_nfa(self) -> NFA:
        """
        Converts the NFA-e to an equivalent NFA by removing epsilon transitions.
        :return: An instance of NFA.
        """
        new_transitions = {}
        for state in self.states:
            closure = self._epsilon_closure({state})
            new_transitions[state] = {}
            for symbol in self.alphabet:
                if symbol == 'ε':
                    continue
                reachable_states = set()
                for s in closure:
                    reachable_states.update(self.transitions.get(s, {}).get(symbol, set()))
                new_transitions[state][symbol] = reachable_states

        new_accept_states = {state for state in self.states if self._epsilon_closure({state}) & self.accept_states}

        return NFA(
            states=self.states,
            alphabet=self.alphabet - {'ε'},
            transitions=new_transitions,
            start_state=self.start_state,
            accept_states=new_accept_states,
        )
    
    def to_dfa(self) -> "DFA":
        """
        Converts the NFA-e to an equivalent DFA using the subset construction algorithm.
        :return: An instance of DFA.
        """
        from collections import defaultdict
        dfa_states = []
        dfa_transitions = {}
        dfa_start_state = frozenset(self._epsilon_closure({self.start_state}))
        unmarked_states = [dfa_start_state]
        dfa_states.append(dfa_start_state)

        while unmarked_states:
            current = unmarked_states.pop()
            dfa_transitions[current] = defaultdict(set)

            for symbol in self.alphabet - {'ε'}:
                next_states = set()
                for state in current:
                    next_states.update(self.transitions.get(state, {}).get(symbol, set()))
                closure = frozenset(self._epsilon_closure(next_states))

                if closure not in dfa_states:
                    dfa_states.append(closure)
                    unmarked_states.append(closure)

                dfa_transitions[current][symbol] = closure

        dfa_accept_states = {state for state in dfa_states if state & self.accept_states}

        return DFA(
            states={frozenset(state) for state in dfa_states},
            alphabet=self.alphabet - {'ε'},
            transitions={
                frozenset(state): {symbol: frozenset(next_states) for symbol, next_states in trans.items()}
                for state, trans in dfa_transitions.items()
            },
            start_state=dfa_start_state,
            accept_states={frozenset(state) for state in dfa_accept_states},
        )
