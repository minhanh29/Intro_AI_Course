This program creates an AI to rank web pages by importance.

An “important” page is the one that many other pages link to, since it’s reasonable to imagine that more sites will link
to a higher-quality webpage than a lower-quality webpage.

The PageRank algorithm was created by Google’s co-founders (including Larry Page, for whom the algorithm was named). In
PageRank’s algorithm, a website is more important if it is linked to by other important websites, and links from less important websites have
their links weighted less.

Type this command to open the program:
python3 pagerank.py corpus#
where # is the index number of package you want to use (0, 1, 2).

Example:
python3 pagerank.py corpus0
Ouput:
PageRank Results from Sampling (n = 10000)
  1.html: 0.2226
  2.html: 0.4288
  3.html: 0.2172
  4.html: 0.1314
PageRank Results from Iteration
  1.html: 0.2211
  2.html: 0.4320
  3.html: 0.2215
  4.html: 0.1319

(The more important page has higher value.)
