import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
SP -> S | S Conj S
AdjP -> Adj | Adj AdjP | Adv Adj
NP -> N | Det N | Det NP | Det AdjP N | NP Conj NP | NP PP
VP -> V | V NP | VP Conj VP | Adv VP | VP Adv | V PP
PP -> P NP | P S
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = [word.lower() for word in nltk.word_tokenize(sentence)\
             if any(c.isalpha() for c in word)]
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    treeQueue = [tree]
    while len(treeQueue) != 0:
        node = treeQueue[0]
        childrenNum = len(node)
        if all(type(node[i]) is not str for i in range(childrenNum)):
            for i in range(childrenNum):
                treeQueue.append(node[i])
            if node.label() == 'NP' and not_contain_NP(node):
                chunks.append(node)
        treeQueue = treeQueue[1:]
    return chunks

def not_contain_NP(node):
    childrenNum = len(node)
    if all(type(node[i]) is not str for i in range(childrenNum)):
        containNP = any(node[i].label() == 'NP' for i in range(childrenNum))
        if not containNP and all(not_contain_NP(node[i]) for i in range(childrenNum)):
            return True
        else:
            return False
    return True

if __name__ == "__main__":
    main()
