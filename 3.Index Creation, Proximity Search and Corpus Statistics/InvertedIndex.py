import os, re
import collections
import ast # for reading stored dicts as text eliminating need for pickle objects

class InvertedIndex:
    def __init__(self, inputDir):
        self.content = {}                                                    # Creating a dictionary for storing content
        self.words = {}                                                      # Creating a dictionary for storing words with keys as files
        for file in os.listdir(inputDir):     # Accesing the parsed text files
            if file != ".DS_Store":                                           # To avoid DS_Store file, if the code is run on mac machines
                with open(inputDir + '/' + file, 'r', encoding ="utf-8") as filein:
                    content = filein.read()
                    file = file.rstrip(".txt")                    # Removing .txt to retrieve DocIDs
                    self.content[file] = content
                    self.words[file] = content.split()

    def indexNTerms(self, n=1):
        count = {}
        for file, words in self.words.items():
            terms = zip(*[words[i:] for i in range(n)])
            count[file] = len(set(terms))
        return count

    def indexFreq(self, n=1):
        index = collections.defaultdict(list)
        for file, words in self.words.items():
            terms = zip(*[words[i:] for i in range(n)])
            count = collections.Counter(terms)
            for term, cnt in count.items():
                index[term].append((file, cnt))
        return dict(index)

    def posIndex(self):
        index = collections.defaultdict(list)
        #index = {}
        for file, words in self.words.items():
            for wd in set(words):     # using set() to avoid creating positions for the same word repeatedly in a file/docID
                position = [pos+1 for pos, term in enumerate(list(words)) if term == wd]
                last_pos = 0;
                encoded_pos= []
                for p in position:            # Delta encoding the postions
                    current = p
                    pos = current - last_pos
                    last_pos = current
                    encoded_pos.append(pos)
                if wd not in index.keys():
                    index[wd] = [(file,encoded_pos)]       # creating the posting
                else:
                    index[wd].append((file, encoded_pos)) # assigning encoded positions with docID as a tuple to Term.
        return dict(index)


    def decodePositions(input):  # creating a method to apply decoding.
        decoded = []
        for d,l in input:
            dec_pos= []
            last_pos = 0
            for p in l:
                delta = p
                p = delta + last_pos
                last_pos = p
                dec_pos.append(p)
            decoded.append((d,dec_pos))
        return list(decoded)      # Decoding the positions and returning the result as a list of tuple of (docID , pos) like original record

    def conjunctiveProximityQuery(self):

        term1 = str(input("Input the first term name for Conjunctive query : "))
        term2 = str(input("Input the second term name for Conjunctive query : "))
        k = int(input("Input positional diff 'k' for Conjunctive query (i.e wordcount BETWEEN terms) : "))
        #index = indexer.posIndex()             # directly load the index from posindex()

        with open("indexes/posindex(Task-1d).txt", 'r', encoding ="utf-8") as filein:           # loading the index from disk
            index = ast.literal_eval(filein.read())

        record1 = index[term1]
        record2 = index[term2]


        q1 = InvertedIndex.decodePositions(record1)
        q2 = InvertedIndex.decodePositions(record2)


        matched_query = [(d1) for (d1,p1) in q1 for (d2,p2) in q2 if ((d1==d2) & bool([True for i in p1 for j in p2 if (abs(i-j) == k+1)]))]
        # complete doc matching and pos proximity check done in one line of comprehension.

        # Not storing positions since we only need to find if the query terms occurs in the document within proximity or not.(Plus it wasnt asked in Question)

        # q1 = First term / query      # d1 = documents containing q1     # p1 = list of positions for term in d1
        # q2 = Second term / query     # d2 = documents containing q2     # p2 = list of positions for term in d2
        if matched_query == []:
            print("---------------- No document match found for that term proximity (check gaps or try diff k)  -------------------")


        return(matched_query)

#------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    folder = str(input("Input the folder name with parsed documents (keep folder in cwd) : "))
    indexer = InvertedIndex(folder)

    if not os.path.exists("indexes"):
        os.mkdir("indexes")

    ngram_range = int(input("Enter the value of n to set range ie. 3 for 1,2,3 : n = "))
    for n in range(1,ngram_range+1):
        with open("indexes/nterms" + str(n) + ".txt", "w+",encoding = "utf-8") as fout:
            fout.write(str(indexer.indexNTerms(n)))
        with open("indexes/freq" + str(n) + ".txt", "w+",encoding = "utf-8") as fout:
            fout.write(str(indexer.indexFreq(n)))

    with open("indexes/posindex(Task-1d).txt", "w+", encoding = "utf-8") as fout:
        fout.write(str(indexer.posIndex()))
    with open("indexes/conjunctive_query(Task-2).txt", "w+", encoding = "utf-8") as fout:
        fout.write(str(indexer.conjunctiveProximityQuery()))
