# Homework 2

All files to be run on python 3
Libraries : import os
            import glob
            from time import sleep
            import requests
            from bs4 import BeautifulSoup
            import nltk
            from nltk.tokenize import word_tokenize
            import string
            import pandas
            import matplotlib.pyplot as plt
            from collections import defaultdict


## Task - 1
  Parsing/Cleaning downloaded HTML files and Tokenizing

- run 'downloadHTML.py' and specify source link file (BFS/FOCUSED.txt) which will create corresponding folders (htmls/fhtml)
- run 'ParseAndTokenize.py' to get cleaned articles/corpus in (htmls/fhtmls_parsed_text)  and Trigrams freq file (takes 5-7 mins)

## Task -2
  Building Graphs G1 and G2
- Run 'createGraph.py'
- Enter input/output filenames as prompted
- It takes a while to graph the 1000 links.
- Check the output file for the in-link-format graph.


## Task -3 & 4
  PageRank Algorithm
- Run 'python PageRank.py' and input the graph name which should be in cwd.
- Graph Statistics are stored in G1/G2 Statistics.txt
- For different answers pertaining to problems in Task 4 ,Follow the comment in main function in `PageRank.py` to run one line and comment out the others
- Enter k for Top k results
- give output filenames as prompted for PR and L2norm.
- Check output files for ranking and L2norm.
