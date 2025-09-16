# NFA to DFA converter based on the subset construction from the notes
# No epsilon transitions, as per the problem
# Using tuples for subsets since sets aren't hashable easily without frozenset
# Kept it simple, like sketching it out on paper

class NFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function  # dict of (state, sym): set of states
        self.start_state = start_state
        self.accept_states = set(accept_states)  # Using set here for quick lookup
        self.current_states = [start_state]

    def transition_on_input(self, input_value):
        new_states = []
        for state in self.current_states:
            key = (state, input_value)
            if key in self.transition_function:
                for next_state in self.transition_function[key]:
                    if next_state not in new_states:
                        new_states.append(next_state)
        self.current_states = new_states

    def in_accept_state(self):
        for state in self.current_states:
            if state in self.accept_states:
                return True
        return False

    def accept(self, word):
        self.current_states = [self.start_state]
        for char in word:
            self.transition_on_input(char)
        return self.in_accept_state()
    
    

    def dfa(self):
        # convert NFA to DFA using subset construction
        start_set = tuple([self.start_state])  # tuple so we can use as dict key

        # Use a list as queue for BFS
        to_process = [start_set]
        visited = {start_set}
        all_sets = [start_set]
        transitions = {}
        
        # BFS through all possible state combinations
        while to_process:
            current = to_process.pop(0)
            
            for char in self.alphabet:
                # find all states we can reach from current set on this char
                reachable = []
                for state in current:
                    if (state, char) in self.transition_function:
                        for next_state in self.transition_function[(state, char)]:
                            if next_state not in reachable:
                                reachable.append(next_state)
                
                # sort and make tuple (or empty if no transitions)
                if reachable:
                    next_set = tuple(sorted(reachable))
                else:
                    next_set = ()  # dead state
                
                transitions[(current, char)] = next_set
                
                # add to queue if we haven't seen it
                if next_set not in visited:
                    visited.add(next_set)
                    to_process.append(next_set)
                    all_sets.append(next_set)
        
        # convert tuples to readable state names
        state_map = {}
        for s in all_sets:
            if s == ():
                state_map[s] = 'DEAD'
            else:
                state_map[s] = '{' + ','.join(s) + '}'
        
        # build the actual DFA
        new_states = list(state_map.values())
        new_start = state_map[start_set]
        
        # accepting states = any set containing an NFA accept state
        new_accept = []
        for state_set in all_sets:
            if any(s in self.accept_states for s in state_set):
                new_accept.append(state_map[state_set])
        
        # convert transitions to use new state names
        new_trans = {}
        for (from_set, symbol), to_set in transitions.items():
            from_name = state_map[from_set]
            to_name = state_map[to_set]
            new_trans[(from_name, symbol)] = to_name
        
        # make sure dead state transitions to itself
        if () in state_map:
            dead_name = state_map[()]
            for symbol in self.alphabet:
                new_trans[(dead_name, symbol)] = dead_name
        
        from cps337_dfa import DFA
        return DFA(new_states, self.alphabet, new_trans, new_start, new_accept)


# Test it out with the example from the notes (third 1 from end is 0? Wait, the one in cps337_nfa.py)
if __name__ == "__main__":
    states = ['q1', 'q2', 'q3', 'q4']
    alphabet = ['0', '1']
    transitions = {
        ('q1', '0'): {'q1'},
        ('q1', '1'): {'q1', 'q2'},
        ('q2', '0'): {'q3'},
        ('q2', '1'): {'q3'},
        ('q3', '0'): {'q4'},
        ('q3', '1'): {'q4'}
    }
    start_state = 'q1'
    accept_states = ['q4']

    nfa = NFA(states, alphabet, transitions, start_state, accept_states)

    # Check NFA accepts
    print("NFA accepts '000100':", nfa.accept('000100'))  # Should be True
    print("NFA accepts '0011':", nfa.accept('0011'))      # Should be False

    # Convert to DFA
    dfa = nfa.dfa()

    # Check DFA accepts the same
    print("\nDFA accepts '000100':", dfa.accept('000100'))  # True
    print("DFA accepts '0011':", dfa.accept('0011'))        # False

    # Empty string
    print("DFA accepts '':", dfa.accept(''))                # False, since start doesn't accept

    # Print DFA summary
    print("\nDFA States:", dfa.states)
    print("DFA Start:", dfa.start_state)
    print("DFA Accept:", dfa.accept_states)