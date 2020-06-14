This program generates a crossword puzzle.

Given the structure of a crossword puzzle (i.e., which squares of the grid are meant tobe filled in with a letter), and a list of words to use, the problem becomes one of choosing which words should go in each vertical or horizontal sequence of squares.

Type this command to open the program
python3 generate.py data/structure<#>.txt data/words<#>.txt output<#>.png
where <#> is 0, 1, or 2 (the index of data sets)

Example:
python3 generate.py data/structure1.txt data/words1.txt output1.png

██████████████
███████M████N█
█INTELLIGENCE█
█N█████N████T█
█F██LOGIC███W█
█E█████M████O█
█R███SEARCH█R█
███████X████K█
██████████████