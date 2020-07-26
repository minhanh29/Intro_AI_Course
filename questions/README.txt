This program is a very simple question answering system based on inverse document frequency.

1. Install nltk:
pip3 install nltk

2. Download stopwords data set:
(/Applications/Python\ 3.8/Install\ Certificates.command  - if there is an error)
python3
import nltk
nltk.download('stopwords')

3. Type this command to run the program:
python3 questions.py corpus

Example output:
Query: When was Python 3.0 released?
Python 3.0 was released on 3 December 2008.
Do you want to ask again (y/n)? y

Query: What are classifications for machine learning approaches?
Early classifications for machine learning approaches sometimes divided them into three broad categories,   depending on the nature of the "signal" or "feedback" available to the learning system.
Do you want to ask again (y/n)? n

