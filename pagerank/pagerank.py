import os
import random
import re
import sys
import math
from collections import Counter

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    #number of linked pages 
    linked_num = len(corpus[page])

    # linked pages
    linked_pages = corpus[page]
   
    #rate when 1-d occurs
    additional_rate = (1 - damping_factor) / len(corpus) 
   
    #output dict
    output = {}

    #rate of the linked pages of page
    if (linked_num != 0):
        linked_rate = damping_factor / linked_num
        for key in corpus:
            if key in linked_pages:
                output[key] = additional_rate + linked_rate
            else:
                output[key] = additional_rate 
    else:    
        for key in corpus:
            output[key] = 1.0 / len(corpus)

    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # samples set
    samples = []

    # page names list
    names = []
    for page in corpus:
        names.append(page)
    
    # choose the first sample at random
    samples.append(random.choice(names))
    

    # create other n-1 samples
    for i in range(n-1):
        # previous sample
        previous = samples[-1]

        # transition model
        transition = transition_model(corpus, previous, damping_factor)

        # names of the next pages
        # and their weight
        next_pages = [] 
        weight = []
        for page in transition:
            next_pages.append(page)
            weight.append(transition[page])

        # get the next random page
        next_page = random.choices(next_pages, weights=weight, k=1)[0]
        samples.append(next_page)

    # count the frequency of elements in samples
    counter = dict(Counter(samples))

    # official output
    output = {}

    # convert numbers into ratio
    for page in counter:
        output[page] = float(counter[page])/n 

    return output



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    VALUE_CHANGE = 0.001

    #current rank and new rank values
    current = {}
    new_rank = {}

    #initialize all values to 1/N
    n = len(corpus)
    first_rate = 1.0 / n 
    default_rate = (1 - damping_factor) / n 

    for page in corpus:
        current[page] = first_rate
        new_rank[page] = 2.0

    #flag to indicate when the value changes < 0.001
    small_enough = False

    while not small_enough: 
        # assume that the value changes < 0.001, we'll check it later
        small_enough = True

        for page in corpus:
            other_pr = 0
            for other in corpus:
                if len(corpus[other]) == 0:
                    other_pr += current[other] / n
                elif page in corpus[other]:
                    other_pr += current[other] / len(corpus[other])
            
            #update new rank
            new_rank[page] = (1 - damping_factor)/n + damping_factor * other_pr

            # if the value changes are still not less than 0.001, then continue looping
            if math.fabs(new_rank[page] - current[page]) > VALUE_CHANGE:
                small_enough = False

            # update current rank
            current = new_rank.copy()
           
    return new_rank



if __name__ == "__main__":
    main()
