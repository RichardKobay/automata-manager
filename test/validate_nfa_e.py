import unittest
from models.nfa_e import NFAE  
class TestNFAEValidation(unittest.TestCase):
    def setUp(self):
        """
        Set up a sample NFA-ε for testing.
        """
        # Define a simple NFA-ε for testing
        self.nfa_e = NFAE(
            states={"q0", "q1", "q2", "q3", "q_accept"},
            alphabet={"a", "b"},
            transitions={
                "q0": {"ε": {"q1"}, "a": {"q2"}},  # ε transition from q0 to q1
                "q1": {"b": {"q2"}},  # Transition on 'b' from q1 to q2
                "q2": {"ε": {"q3"}},  # ε transition from q2 to q3
                "q3": {"a": {"q_accept"}},  # Transition on 'a' to accept state
                "q_accept": {}  # Accept state
            },
            start_state="q0",
            accept_states={"q_accept"}
        )

    def test_valid_string_with_epsilon(self):
        """
        Test a valid string accepted by the NFA-ε using epsilon transitions.
        """
        input_string = "ba"
        self.assertTrue(self.nfa_e.validate_string(input_string), f"String '{input_string}' should be accepted.")

    def test_invalid_string_with_epsilon(self):
        """
        Test an invalid string that should be rejected by the NFA-ε.
        """
        input_string = "bb"
        self.assertFalse(self.nfa_e.validate_string(input_string), f"String '{input_string}' should be rejected.")

    def test_valid_empty_string_with_epsilon(self):
        """
        Test an empty string, which can be valid if epsilon transitions reach an accept state.
        """
        nfa_e_with_empty_accept = NFAE(
            states={"q0", "q1", "q_accept"},
            alphabet={"a", "b"},
            transitions={
                "q0": {"ε": {"q1"}},  # ε transition from q0 to q1
                "q1": {"ε": {"q_accept"}}  # ε transition to accept state
            },
            start_state="q0",
            accept_states={"q_accept"}
        )
        input_string = ""
        self.assertTrue(nfa_e_with_empty_accept.validate_string(input_string), "Empty string should be accepted due to epsilon transitions to accept state.")

    def test_partial_match_with_epsilon(self):
        """
        Test a string that only partially matches the transitions involving ε.
        """
        input_string = "b"
        self.assertFalse(self.nfa_e.validate_string(input_string), f"String '{input_string}' should be rejected.")

    def test_complex_string_with_epsilon(self):
        """
        Test a more complex string with multiple transitions and ε moves.
        """
        input_string = "baa"
        self.assertTrue(self.nfa_e.validate_string(input_string), f"String '{input_string}' should be accepted.")

    def test_invalid_symbol_with_epsilon(self):
        """
        Test a string containing a symbol not in the alphabet.
        """
        input_string = "bac"
        with self.assertRaises(ValueError):
            self.nfa_e.validate_string(input_string)

    def test_edge_case_only_epsilon_transitions(self):
        """
        Test a case where only ε transitions are used to reach the accept state.
        """
        input_string = ""
        nfa_e_only_epsilon = NFAE(
            states={"q0", "q1", "q_accept"},
            alphabet={"a", "b"},
            transitions={
                "q0": {"ε": {"q1"}},
                "q1": {"ε": {"q_accept"}}
            },
            start_state="q0",
            accept_states={"q_accept"}
        )
        self.assertTrue(nfa_e_only_epsilon.validate_string(input_string), "Empty string should be accepted as the only transitions are epsilon.")

    def test_no_epsilon_usage(self):
        """
        Test a case where the NFA-ε behaves like a standard NFA with no ε transitions used.
        """
        nfa_without_epsilon = NFAE(
            states={"q0", "q1", "q_accept"},
            alphabet={"a", "b"},
            transitions={
                "q0": {"a": {"q1"}},
                "q1": {"b": {"q_accept"}}
            },
            start_state="q0",
            accept_states={"q_accept"}
        )
        input_string = "ab"
        self.assertTrue(nfa_without_epsilon.validate_string(input_string), f"String '{input_string}' should be accepted without using ε transitions.")

if __name__ == "__main__":
    unittest.main()
