
==========================================================================================
Deliverable:
1. Source Code:
To run Tasks:
Run Task1.java for task 1.
- put path to save index files
- search results are saved in lucene_search_results ... (keep the folder and dele the txt files if checking need to done otherwise 
Run Task2.py for task 2a.
And Re run Task1.java with changes with queries.txt file  and change paths in task1.java for task 2b

3. The top 100 results for each of the 5 queries from task 1b):
Available in Out_Files Folder -> Task 1.b Files Folder -> The urls for top 100 hits.

4. The list of expansion terms identified for each of 5 queries along with the values used for
k and n, in a single text file:
File Name -> Expansion Terms.txt

5. The top 100 results for each of the 5 queries from task 2b), after incorporating query
expansion:
In Out_Files Folder -> Under each Query name folder , the file names has k and n values appended that are used to generate the files.

6. Analysis of the results from Task 3.
In Task 3.txt file
===========================================================================================
Other Files:
1. Corpus:
corpus Folder has the corpus i.e., 1000 text files.

2. TermFrequencies Folder ->  Under Query term name as folder -> This has term frequencies for k=5,10,15.
Example: termFrequency5Mars exploration : Represents MarsExploration Query and k = 5.
Note: The stop words have been removed for all the documents. Using nltk stopwords.

3. Indexed Files Indexed.
=============================================================================================
How to run program?

To run 1 a & 1 b:
Before running program:
Add the queries you want to generate the indexed files in Queries.txt file.
While running program:
1. Give the location where you want to save the generated indexes.
2. Give the location where the corpus is located.
The files will be created in Out_Files Folder.

To run 2 a:
Run Task2.py, to change k value change index attribute in the main file.

To run 2 b:
Get the top 8 top ranked words from term frequency files generated.
and append them to Queries.txt with the original query and run the same steps as task 1a.

============================================================================================
Design choices:

I have used index value to pick the lines from the generated files instead of generating 10,5, 15 urls and
running tak 3 on it. This made my work a lot easier and effective.

I have used nltk stop words, to remove unnecessary words, hence I was able to pick appropriate values
for retrieving relevant query terms.

I have also made inputting my queries as text file, hence making my input completely independent from th
the code.

For task 3, I have used n values as 6,7, 8 and k values as 5, 10, 15 to analyize and experiment with k values and
n values.
