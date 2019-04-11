# Retrieval and scoring using BM25. with comparison to Lucene.

Required python libraries
- pip3 install Collections
- pip3 install ast
- pip3 install pandas

## Task 1
- put corpus into `corpus/
-run `python Task1_BM25.py`

- enter the index file name "bm25index" (which should be preferably in cwd) 
- enter the folder name where the corpus is located (which should be preferably in cwd)
- Enter information as prompted ( 1 for loading from querylist.txt file 2 for individual queries)


NOTE: since the index is large and is being read from disk, the machine running may give out a MemoryError (especially if run from cmd window) while loading the index which is due to the RAM constraint of that specific machine. (use Pycharm/Jupyter to avoid this)

-results are stored in Task-1 rankings

## Task 2

- include `lib` as dependencies

- run `src/Task1.java`

- enter information as prompted for each individual queries
- files with rankings will be saved in cwd

NOTE: when rerunning for different queries do not add the corpus again if using the previously created index this will result in duplicate document rankings