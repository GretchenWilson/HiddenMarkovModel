from HiddenMarkovModel import HMM
import doctest

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
