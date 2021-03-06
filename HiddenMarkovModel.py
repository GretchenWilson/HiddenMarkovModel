from __future__ import division
from copy import deepcopy
from math import log
from Log_Float import log_float
from math.pylab import *
import doctest

class HMM(object):
    """
Docstring for testing HMM class
>>> A = HMM("_14223453452666665656626646643666345263452341263")
>>> forward_value = A.forward()
>>> print (forward_value)
3.68371784339e-34
>>> viterbi_prob, MPS_path = A.viterbi()
>>> print (viterbi_prob)
1.58772133063e-35
>>> print(A.sequence + '\\n' + ''.join(MPS_path))
_14223453452666665656626646643666345263452341263
SFFFFFFFFFFFFFLLLLLLLLLLLLLLLLLLLLLLFLLFFFFFFFFF
1263
"""

    def __init__(self, sequence=None, states=None, emissions=None):

        self.sequence = sequence
        self.sequence_len = len(sequence)

        if states:
            self.states = states

        else:
            self.states = {
                "S": {
                    "F": 0.5,
                    "L": 0.5,
                    },
                "F": {
                    "F": 0.95,
                    "L": 0.05,
                    },
                "L": {
                    "L": 0.90,
                    "F": 0.10,
                    }
            }

        if emissions:
            self.emissions = emissions
        else:
            self.emissions = {

                "S":
                    {
                        "_": 1
                    },
                "F":  # 'F' indicates a fair die
                    {
                        "1": 1 / 6,
                        "2": 1 / 6,
                        "3": 1 / 6,
                        "4": 1 / 6,
                        "5": 1 / 6,
                        "6": 1 / 6
                    },
                "L":  # 'L' indicates a loaded die
                    {
                        "1": 1 / 10,
                        "2": 1 / 10,
                        "3": 1 / 10,
                        "4": 1 / 10,
                        "5": 1 / 10,
                        "6": 1 / 2
                    }
            }
        self.nonstart_states = deepcopy(self.emissions)
        del self.nonstart_states['S']

        # logfloat EVERYTHING!
        for state in self.states:
            for transition_state in self.states[state]:
                self.states[state][transition_state] = log_float(self.states[state][transition_state])

        for state in self.emissions:
            for emission in self.emissions[state]:
                self.emissions[state][emission] = log_float(self.emissions[state][emission])

        # Data tables necessary for this class
        self.forward_table = [{} for k in range(self.sequence_len)]
        self.backward_table = [{} for k in range(self.sequence_len)]     # You can define these later
        self.viterbi_table = [{} for k in range(self.sequence_len)]
        self.posterior_table = [{} for k in range(self.sequence_len)]

        return

     def train_most_likely(self, training_data):
        """ Evaluates given training data to determine state transition and emission probabilities """

        state_symbol_dict = {k: {} for k in self.transitions.keys()}
        state_transition_dict = {k: {} for k in self.transitions.keys()}
        total_state_transition_counts = {k: 0 for k in self.transitions.keys()}
        total_state_emission_counts = {k: 0 for k in self.transitions.keys()}

        for symbol_seq, state_seq in training_data:
            if len(symbol_seq) != len(state_seq):
                continue

            for position in range(len(symbol_seq) - 1):
                # set variables for this position

                cur_state = state_seq[position]
                next_state = state_seq[position + 1]
                emitted_symbol = symbol_seq[position + 1]

                # increment counts
                total_state_transition_counts[cur_state] += 1
                total_state_emission_counts[next_state] += 1
                
                try:
                    state_symbol_dict[cur_state][emitted_symbol] += 1
                except KeyError:
                    state_symbol_dict[cur_state][emitted_symbol] = 0
                try:
                    state_transition_dict[cur_state][next_state] += 1
                except KeyError:
                    state_transition_dict[cur_state][next_state] = 0
                    
        for state in state_symbol_dict:
        
            for symbol in state_symbol_dict[state]:
                if state is "S":
                    state_symbol_dict[state][""] = 1
                else:
                    state_symbol_dict[state][symbol] /= total_state_emission_counts[state]
                    
        for state in state_transition_dict:
        
            for state2 in state_transition_dict[state]:
                state_transition_dict[state][state2] /= total_state_transition_counts[state]

        self.transitions = state_transition_dict
        self.emissions = state_symbol_dict

        return self.transitions, self.emissions
        
    def evaluate_path(self, path):
        """Evaluates the probability of a sequence and path given the model"""
        
        joint_probability_of_sequence_and_path = 1

        for position in range(self.sequence_len - 1):
            old_state = path[position]
            new_state = path[position + 1]

            trans_prob = self.states[old_state][new_state]
            emission = self.sequence[position + 1]
            emission_prob = self.emissions[new_state][emission]
            joint_probability_of_sequence_and_path *= trans_prob * emission_prob

        return joint_probability_of_sequence_and_path
        
    def viterbi(self):

        possible_paths = {k: ['S'] for k in self.nonstart_states}
        self.viterbi_table[0] = {'S': 1}

        for position in range(1, self.sequence_len):
            prev_position = position - 1
            symbol = self.sequence[position]
            prev_vks = self.viterbi_table[prev_position]
            position_vks = []

            for state in possible_paths:
                vks = []
                emission = self.emissions[state][symbol]

                for old_state in prev_vks:
                    old_state_vk = prev_vks[old_state]
                    transition_prob = self.states[old_state][state]
                    new_transition_vk = old_state_vk * transition_prob
                    vks.append(new_transition_vk)

                max_state_vk = max(vks) * emission
                position_vks.append([max_state_vk, state])
                self.viterbi_table[position][state] = max_state_vk

            max_position_vk, max_state = max(position_vks)

            for path in possible_paths:
                possible_paths[path].append(max_state)

        return (max((self.viterbi_table[self.sequence_len-1][state],
                possible_paths[state]) for state in possible_paths))
          
    def forward(self):
    
        self.forward_table[0] = {'S': 1}  # Start position 0 has Fk of 1

        for position in range(1, self.sequence_len):
            prev_position = position - 1
            prev_fks = self.forward_table[prev_position]
            symbol = self.sequence[position]

            for new_state in self.nonstart_states.keys():
                state_position = 0
                emission_prob = self.emissions[new_state][symbol]
                for old_state in prev_fks:
                    transition_prob = self.states[old_state][new_state]
                    new_fk = prev_fks[old_state] * transition_prob
                    state_position += new_fk
                state_position *= emission_prob
                self.forward_table[position][new_state] = state_position

        # Here is the termination. Note that if you have iterated over position
        return sum([self.forward_table[self.sequence_len - 1][state] for state in self.forward_table[self.sequence_len - 1]])

    def backward(self):

        self.backward_table[self.sequence_len-1] = {state: 1 for state in self.nonstart_states}  # Start position 0 has Fk of 1

        for new_position in xrange(self.sequence_len -1, 0, -1):
            old_position = new_position - 1
            prev_fks = self.backward_table[new_position]
            symbol = self.sequence[new_position]

            for old_state in self.nonstart_states.keys():
                state_position = 0

                for new_state in prev_fks:
                    emission_prob = self.emissions[new_state][symbol]
                    transition_prob = self.states[old_state][new_state]
                    new_fk = prev_fks[new_state] * transition_prob * emission_prob
                    state_position += new_fk
                    print "\n", old_state, " ->", new_state, " = ", transition_prob, prev_fks[new_state]

                self.backward_table[old_position][old_state] = state_position


        backwards_variable = 0
        for new_state in self.backward_table[1:
            prev_fk = self.backward_table[1][new_state]
            symbol = self.sequence[1]
            emission = self.emissions[new_state][symbol]
            transition = self.states['S'][new_state]
            backwards_variable += transition * prev_fk * emission
        self.backward_table[0] = backwards_variable

        return self.backward_table[0]          
     

if __name__ == "__main__":

    doctest.testmod()
    A = HMM("_14223453452666665656626646643666345263452341263")

    forward_a = A.forward()
    # # 3.68371784339e-34
    viterbi_a, MPS_path = A.viterbi()
    # # 1.58772133063e-35
    backwards_a = A.backward()
    print(A.sequence + '\n' + ''.join(MPS_path))
    print "Forward: ", forward_a
    print "Viterbi: ", viterbi_a
    print "Backwards: ", backwards_a

    evaluate_a = A.evaluate("SFFFFFFFFFFFFFLLLLLLLLLLLLLLLLLLLLLLFLLFFFFFFFFF")
    fair_probability = A.evaluate("SFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    loaded_probability = A.evaluate("SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
    print "Viterbi Path Log: ", viterbi_a.value
    print "Evaluate Fair Path Log: ", fair_probability.value
    print "Evaluate Loaded Path Log: ", loaded_probability.value

    sequence = "_CCGTATACGCGACAGCAAATTTTGACAATATAACATGAATTTTACGGGGCACGCATGCCACC"

    states = {
        "S": {
            "+": 0.5,
            "-": 0.5,
        },
        "+": {
            "+": 0.85,
            "-": 0.15,
        },
        "-": {
            "-": 0.95,
            "+": 0.05,
        }
    }

    emissions = {

        "S":
            {
                "_": 1
            },
        "-":
            {
                "A": 0.1,
                "C": 0.40,
                "G": 0.40,
                "T": 0.1,

            },
        "+":
            {
                "A": 0.35,
                "C": 0.20,
                "G": 0.10,
                "T": 0.35,
            }
    }

    B = HMM(sequence, states, emissions)
    b_forward = B.forward()
    b_prob, b_path = B.viterbi()
    print("\n" + B.sequence + "\n" + "".join(b_path) + "\n" + str(b_prob))
    eval_b = B.evaluate("S++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print "Forward: ", b_forward
    print "Viterbi: ", b_prob
    print "Viterbi Log: ", b_prob.value
    print "Evaluate log: ", eval_b.value 
