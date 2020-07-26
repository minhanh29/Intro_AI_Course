import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    choice = 'y'
    while (choice.lower() == 'y'):
        # Prompt user for query
        query = set(tokenize(input("Query: ")))

        # Determine top file matches according to TF-IDF
        filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

        # Extract sentences from top files
        sentences = dict()
        for filename in filenames:
            for passage in files[filename].split("\n"):
                for sentence in nltk.sent_tokenize(passage):
                    tokens = tokenize(sentence)
                    if tokens:
                        sentences[sentence] = tokens

        # Compute IDF values across sentences
        idfs = compute_idfs(sentences)

        # Determine top sentence matches
        matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
        for match in matches:
            print(match)

        choice = input("Do you want to ask again (y/n)? ")
        print()


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for file in os.listdir(directory):
        with open(os.path.join(directory, file)) as f:

            # Extract contents
            files[file] = f.read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    contents = [word.lower() for word in nltk.word_tokenize(document)
                if word not in string.punctuation
                and word not in nltk.corpus.stopwords.words("english")]

    return contents


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # count the number of files that contain word
    num_file = dict()
    for file in documents:
        for word in documents[file]:
            if word not in num_file:
                num_file[word] = 0
                for file in documents:
                    if word in documents[file]:
                        num_file[word] += 1

    # compute the idfs
    idfs = dict()
    for word in num_file:
        idfs[word] = math.log(len(documents) / num_file[word])

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    sorted_files = list()
    unsorted_files = dict()

    # count the word frequencies in each file
    for file in files:
        unsorted_files[file] = 0
        for word in query:
            if word in files[file]:
                frequency = files[file].count(word)
                unsorted_files[file] += frequency * idfs[word]

    # sort the list via dict's values
    count = 0
    for file, content in sorted(unsorted_files.items(),
                                key=lambda item: item[1],
                                reverse=True):
        sorted_files.append(file)
        count += 1
        if (count == n):
            break

    return sorted_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sorted_sentences = list()
    unsorted_sentences = dict()

    # compute IDF values
    for sentence in sentences:
        unsorted_sentences[sentence] = 0
        for word in query:
            if word in sentences[sentence]:
                unsorted_sentences[sentence] += idfs[word]

    # compute word density
    density_sentences = dict()
    for sentence in sentences:
        density = 0
        for word in sentences[sentence]:
            if word in query:
                density += 1
        density_sentences[sentence] = density / len(sentences[sentence])

    # sort the sentence
    count = 0
    for key, value in sorted(unsorted_sentences.items(),
                             key=lambda item:
                             (item[1], density_sentences[item[0]]),
                             reverse=True):
        sorted_sentences.append(key)
        count += 1
        if count == n:
            break

    return sorted_sentences


if __name__ == "__main__":
    main()
