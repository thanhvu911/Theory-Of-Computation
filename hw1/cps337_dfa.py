#!/usr/bin/python
# -*- coding: latin-1 -*-

# Deterministic Finite Automata (DFA) implementation in python

#Orignal Author: Earl Austin Zuniga
#Bicol University
#
#Edits:  Justin Brody; Franklin and Marshall College

import os,sys

# DFA Function: check if language is in DFA machine
class DFA:
    #initialize all variable when calling the class DFA
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state
        return

    #check if input in transition function initialize
    def transition_to_state_with_input(self, input_value):
        if ((self.current_state, input_value) not in self.transition_function.keys()):
            self.current_state = None
        else:
            self.current_state = self.transition_function[(self.current_state, input_value)]


    def in_accept_state(self):
        return self.current_state in self.accept_states

    #run the given word through the DFA and return TRUE if it is accepted; FALSE otherwise
    def accept(self, word):
        self.current_state = self.start_state
        for char in word:
            self.transition_to_state_with_input(char)
            continue
        return self.in_accept_state()

