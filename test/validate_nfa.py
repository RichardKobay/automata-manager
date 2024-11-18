import unittest
from models.nfa import NFA

class TestNFAValidation(unittest.TestCase):
    def setUp(self):
        """
        Set up a sample NFA for testing.
        """
        # Define a simple NFA for testing
        self.nfa = NFA(
            states={"q0", "q1", "q2", "q_intermediate", "q_accept"},
            alphabet={"a", "b"},
            transitions={
                "q0": {"b": {"q1"}, "a": {"q2"}},
                "q1": {"a": {"q2"}},
                "q2": {"b": {"q0", "q_intermediate"}},  # q2 can loop or move forward
                "q_intermediate": {
                    "b": {"q_accept"},  # Final "b" leads to acceptance
                    "a": {"q2"}  # Loop back to q2 on "a"
                },
                "q_accept": {}  # Accept state
            },
            start_state="q0",
            accept_states={"q_accept"}
        )

    def test_valid_string(self):
        """
        Test a valid string accepted by the NFA.
        """
        input_string = "abb"
        self.assertTrue(self.nfa.validate_string(input_string), f"String '{input_string}' should be accepted.")

    def test_invalid_string(self):
        """
        Test an invalid string rejected by the NFA.
        """
        input_string = "aaa"
        self.assertFalse(self.nfa.validate_string(input_string), f"String '{input_string}' should be rejected.")

    def test_empty_string(self):
        """
        Test an empty string (edge case).
        """
        input_string = ""
        self.assertFalse(self.nfa.validate_string(input_string), "Empty string should be rejected unless q0 is an accept state.")

    def test_partial_input(self):
        """
        Test a string that only partially matches the transitions.
        """
        input_string = "ab"
        self.assertFalse(self.nfa.validate_string(input_string), f"String '{input_string}' should be rejected.")

    def test_edge_case(self):
        """
        Test an edge case with repeated transitions.
        """
        input_string = "bababab"
        self.assertTrue(self.nfa.validate_string(input_string), f"String '{input_string}' should be accepted.")

    def test_invalid_symbol(self):
        """
        Test a string containing a symbol not in the alphabet.
        """
        input_string = "abc"
        with self.assertRaises(ValueError):
            self.nfa.validate_string(input_string)

if __name__ == "__main__":
    unittest.main()
