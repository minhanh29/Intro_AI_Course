This program use the context-free grammar formalism to parse English sentences to determine their structure.
Then, it will print out all the noun chunk (noun phrases that do not contain other noun phrases).

Type this command to open the program:
python3 parser.py [file name]

If [file name] is not specified, the program will let the user type his or her own sentence.


Sample output:
python3 parser.py sentences/5.txt
                    S
      ______________|_________
     |                        VP
     |               _________|_______
     |              |                 NP
     |              |      ___________|________
     NP             |     |          AdjP      |
  ___|______        |     |           |        |
Det         N       V    Det         Adj       N
 |          |       |     |           |        |
 my     companion smiled  an     enigmatical smile

Noun Phrase Chunks
my companion
an enigmatical smile
                    S
      ______________|_________
     |                        VP
     |               _________|_______
     NP             |                 NP
  ___|______        |      ___________|________
 |          NP      |     |          AdjP      |
 |          |       |     |           |        |
Det         N       V    Det         Adj       N
 |          |       |     |           |        |
 my     companion smiled  an     enigmatical smile

Noun Phrase Chunks
companion
an enigmatical smile


