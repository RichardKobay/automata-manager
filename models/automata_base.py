# automata_base.py

from typing import Set, Dict, Any
from graphviz import Digraph

class AutomatonBase:
    """
    Base class for finite automata.
    """
    def __init__(self, states: Set[str], alphabet: Set[str], transitions: Dict[str, Dict[str, Set[str]]], 
                start_state: str, accept_states: Set[str]):
        """
        Initializes the automaton.
        
        :param states: Set of states in the automaton
        :param alphabet: Set of symbols in the input alphabet
        :param transitions: Transition function (state -> symbol -> next states)
        :param start_state: Initial state of the automaton
        :param accept_states: Set of accept (final) states
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self._validate_automaton()

    def _validate_automaton(self):
        """
        Validates the structure of the automaton to ensure consistency and detect potential issues.
        """
        # Validate start and accept states
        if self.start_state not in self.states:
            raise ValueError("Start state must be one of the defined states.")

        if not self.accept_states.issubset(self.states):
            raise ValueError("Accept states must be a subset of the defined states.")

        # Validate transitions
        for state, transitions in self.transitions.items():
            if state not in self.states:
                raise ValueError(f"State {state} in transitions is not defined in states.")

            for symbol, next_states in transitions.items():
                if symbol not in self.alphabet and symbol != 'ε':  # ε for epsilon transitions
                    raise ValueError(f"Symbol {symbol} in transitions is not in the alphabet.")
                if not next_states.issubset(self.states):
                    raise ValueError(f"Next states {next_states} in transitions are not defined in states.")

        # Check for unused states
        used_states = {self.start_state} | self.accept_states
        for state, transitions in self.transitions.items():
            for next_states in transitions.values():
                used_states.update(next_states)
        unused_states = self.states - used_states
        if unused_states:
            raise ValueError(f"Unused states detected: {unused_states}")

        # Check for unreachable states
        reachable_states = self._find_reachable_states()
        unreachable_states = self.states - reachable_states
        if unreachable_states:
            raise ValueError(f"Unreachable states detected: {unreachable_states}")

        # Check for circular epsilon transitions (specific to NFAE)
        if 'ε' in self.alphabet or any('ε' in transitions for transitions in self.transitions.values()):
            if self._has_circular_epsilon_transitions():
                raise ValueError("Circular epsilon transitions detected in the automaton.")

    def _find_reachable_states(self) -> set:
        """
        Finds all reachable states starting from the start state.
        """
        reachable = set()
        stack = [self.start_state]

        while stack:
            state = stack.pop()
            if state not in reachable:
                reachable.add(state)
                for transitions in self.transitions.get(state, {}).values():
                    stack.extend(transitions)

        return reachable

    def _has_circular_epsilon_transitions(self) -> bool:
        """
        Detects circular epsilon transitions in the automaton.
        """
        visited = set()

        def dfs(state, path):
            if state in path:  # Circular reference detected
                return True
            if state in visited:
                return False
            visited.add(state)
            path.add(state)

            for next_state in self.transitions.get(state, {}).get('ε', []):
                if dfs(next_state, path):
                    return True

            path.remove(state)
            return False

        for state in self.states:
            if dfs(state, set()):
                return True

        return False

    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the automaton to a dictionary representation (useful for JSON export).
        """
        return {
            "states": list(self.states),
            "alphabet": list(self.alphabet),
            "transitions": {state: {symbol: list(next_states) 
                                    for symbol, next_states in transitions.items()} 
                            for state, transitions in self.transitions.items()},
            "start_state": self.start_state,
            "accept_states": list(self.accept_states),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Creates an automaton from a dictionary representation.
        """
        return cls(
            states=set(data["states"]),
            alphabet=set(data["alphabet"]),
            transitions={state: {symbol: set(next_states) 
                                for symbol, next_states in transitions.items()} 
                        for state, transitions in data["transitions"].items()},
            start_state=data["start_state"],
            accept_states=set(data["accept_states"]),
        )
    
    def pretty_print_transitions(self):
        """
        Prints the transition table of the automaton in a readable format.
        """
        print(f"{'State':<10} {'Symbol':<10} {'Next States':<20}")
        print("=" * 40)
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                print(f"{state:<10} {symbol:<10} {', '.join(next_states):<20}")


    def visualize(self, filename="automaton", format="png"):
        """
        Visualizes the automaton using Graphviz and saves it to a file.

        :param filename: The name of the output file (without extension).
        :param format: The output file format (e.g., 'png', 'pdf').
        """
        dot = Digraph(name=filename, format=format)

        # Add states
        for state in self.states:
            if state in self.accept_states:
                dot.node(state, shape="doublecircle")  # Accept states
            else:
                dot.node(state, shape="circle")

        # Add transitions
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    label = "ε" if symbol == "ε" else symbol
                    dot.edge(state, next_state, label=label)

        # Add start state marker
        start_marker = "start"
        dot.node(start_marker, shape="plaintext", label="")
        dot.edge(start_marker, self.start_state)

        # Render the graph
        dot.render(filename, cleanup=True)
        print(f"Automaton visualization saved to {filename}.{format}")


