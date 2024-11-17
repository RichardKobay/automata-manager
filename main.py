from models.dfa import DFA

# Create a simple DFA for testing
dfa = DFA(
    states={"q0", "q1", "q2"},
    alphabet={"a", "b"},
    transitions={
        "q0": {"a": {"q1"}, "b": {"q2"}},
        "q1": {"a": {"q0"}, "b": {"q2"}},
        "q2": {"a": {"q2"}, "b": {"q0"}}
    },
    start_state="q0",
    accept_states={"q1"}
)

# Pretty print transitions
dfa.pretty_print_transitions()

# Visualize the DFA
dfa.visualize(filename="dfa_example", format="png")
