# Completed NFA (replace the starter in cps337_nfa.py)
class NFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_states = {start_state}
        return

    def transition_on_input(self, input_value):
        # Compute next set of states from current set
        new_states = set()
        for state in self.current_states:
            key = (state, input_value)
            # Check if this state has a transition on this input
            if key in self.transition_function:
                # Add all possible next states (NFA can branch!)
                new_states.update(self.transition_function[key])
        
        self.current_states = new_states

    def in_accept_state(self, accept_states=None):
        # Check if any current state is an accept state
        return bool(self.current_states & self.accept_states)

    def accept(self, word):
        # Helper method to test if a word is accepted
        self.current_states = {self.start_state}
        for char in word:
            self.transition_on_input(char)
        return self.in_accept_state()

# Build the NFA from Example 1.30
states = ['q1', 'q2', 'q3', 'q4']
alphabet = ['0', '1']
transitions = {
    ('q1', '0'): {'q1'},
    ('q1', '1'): {'q1', 'q2'},  # Loop or guess the third-from-end 1
    ('q2', '0'): {'q3'},
    ('q2', '1'): {'q3'},
    ('q3', '0'): {'q4'},
    ('q3', '1'): {'q4'}
}
accept_states = {'q4'}
start_state = 'q1'

n = NFA(states, alphabet, transitions, start_state, accept_states)

def process_word(nfa, word):
    # Reset to start state
    nfa.current_states = {nfa.start_state}
    
    # Process each character and show current states
    for char in word:
        current_list = sorted(list(nfa.current_states))  # Sort for consistent output
        print(f"({current_list}, {char})")
        nfa.transition_on_input(char)
    
    # Show final result
    final_list = sorted(list(nfa.current_states))
    print(f"({final_list}, <E>)")
    accepted = nfa.in_accept_state()
    print(f"Final states: {nfa.current_states}, Accepted: {accepted}")

# Trace the inputs
print("Processing '000100':")
process_word(n, '000100')

print("\nProcessing '0011':")
process_word(n, '0011')