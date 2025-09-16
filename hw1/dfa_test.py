from cps337_dfa import DFA

states = ['q0', 'q1']
alphabet = ['0', '1']
transitions = {
    ('q0', '0'):  'q1',
    ('q0', '1'):  'q0',
    ('q1', '0'):  'q1',
    ('q1', '1'):  'q0'
}
accept_states = ['q1']
start_state = 'q0'

d = DFA(states, alphabet, transitions, start_state, accept_states)
print(d.accept("011"))   # Should be false
print(d.accept("0110"))  # Should be true
