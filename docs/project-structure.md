# Module details

`main.py`: Starts the application and sets the main window.

`gui/`

- `main_window.py`: This is the main interface window, providing navigation for the user to switch between automata input, validation and conversion views.
- `automata_input_view.py`: A view for entering automata configurations (NFA, NFA-e) and strings for validation.
- `conversion_view.py`: Allows users to enter regular expressions or automata and select conversions.
- `components/`
    - `automata_editor.py`: Graphical component for displaying and editing automata.
    - `automata_input_form.py`: Form widget for capturing input strings or automata.
    - `conversion_controls.py`: Controls to manage available conversions.

`controllers/`
- `main_controller.py`: Manages view switching and overall application control.
- `automata_controller.py`: Handles automata operations, such as creating and validating NFA/NFA-e based on user input.
- `conversion_controller.py`: Manages automata conversions, interacting with the conversion service.

`models/`
- `automata_base.py`: A base class defining common attributes (states, transitions) and methods for automata.
- `nfa.py`, `nfa_e.py`, `dfa.py`: Models to encapsulate the specific details of each automaton type, including methods for validation and conversion.
- `regex.py`: Handles regular expression representation and parsing.

`services/`
- `validation_service.py`: Provides validation of input strings for NFA/NFA-e using their transition functions.
- `conversion_service.py`: Performs automata conversions, such as:
    - Regular expression to NFA-e/NFA
    - NFA-e to NFA
    - NFA to DFA
- `parser.py`: Parses regular expressions into token structures suitable for automata conversion.

`utils/`
- `automata_drawer.py`: Optional utility to visualize automata structures, potentially using libraries like graphviz.
- `file_handler.py`: Manages file operations, such as saving and loading automata configurations.
