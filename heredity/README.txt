Given information about people, who their parents are, and whether they have a particular observable trait 
(e.g. hearing loss)caused by a given gene, the AI will infer the probability distribution for each
person’s genes, as well as the probability distribution for whether any person will exhibit the trait in question.

Open the program by typing this command
python3 heredity.py data/family0.csv  

(change family0 to family1 or family2 to open those data sets)
 Example output:
 Harry:
  Gene:
    2: 0.3652
    1: 0.6292
    0: 0.0056
  Trait:
    True: 0.5600
    False: 0.4400
James:
  Gene:
    2: 0.1976
    1: 0.5106
    0: 0.2918
  Trait:
    True: 1.0000
    False: 0.0000
Lily:
  Gene:
    2: 0.0036
    1: 0.0136
    0: 0.9827
  Trait:
    True: 0.0000
    False: 1.0000
