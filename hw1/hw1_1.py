# Import the DFA class (assuming cps337_dfa.py is in the same directory)
from cps337_dfa import DFA  # Or paste the DFA class definition here if needed

states = ['q0', 'q1', 'q2', 'q3']
alphabet = ['a', 'b']
transitions = {
    ('q0', 'a'): 'q1',
    ('q0', 'b'): 'q0',
    ('q1', 'a'): 'q1',  # Still ends with 'a'
    ('q1', 'b'): 'q2',
    ('q2', 'a'): 'q3',  # Got "aba"!
    ('q2', 'b'): 'q0',  # Reset
    ('q3', 'a'): 'q3',
    ('q3', 'b'): 'q3'
}
accept_states = ['q3']
start_state = 'q0'

d = DFA(states, alphabet, transitions, start_state, accept_states)

def process_word(dfa, word):
    # Reset to start state first
    dfa.current_state = dfa.start_state
    
    # Process each character and show the trace
    for char in word:
        print(f"({dfa.current_state}, {char})")
        dfa.transition_to_state_with_input(char)
    
    # Show final state
    print(f"({dfa.current_state}, ε)")   # <E> represents end of input
    result = dfa.in_accept_state()
    print(f"Final state: {dfa.current_state}, Accepted: {result}")
    print()

# Run the traces
print("Processing 'abb':")
process_word(d, 'abb')

print("\nProcessing 'bbabab':")
process_word(d, 'bbabab')