from math import log
import os
from os import listdir
from collections import Counter
from collections import defaultdict
import ast # for reading stored dicts as text eliminating need for pickle objects
import pandas # for data frames


SYSTEM_NAME = "Akshay_BM25"
K1 = 1.2
B = 0.75
K2 = 100
R = RI = 0

class BM25:
    def __init__(self, corpusDir, indexFile):
        self.readIndex(indexFile)
        self.readCorpus(corpusDir)

    def readIndex(self, filename):
        with open(filename+".txt", 'r',encoding= "utf-8") as fin:
            self.index = ast.literal_eval(fin.read())

    def readCorpus(self, dir):
        self.avglen = 0
        self.length = defaultdict(int)
        for file in listdir(dir):
            if file != ".DS_Store":
                with open(dir + '/' + file, 'r', encoding = "utf-8") as fin:
                    file = file.rstrip(".txt")
                    l = len(fin.read().split())
                    self.avglen += l
                    self.length[file] = l
        self.N = len(self.length)
        self.avglen /= self.N

    def computeBM25(self, file, query):
        bm25score = 0  # setting initial score to 0
        K = K1 * ((1 - B) + B * self.length[file] / self.avglen)
        for w in query.split():
            for w in query.split():
                if (w,) in self.index:
                    for f,n in self.index[(w,)]:
                        if f == file:
                            tf = n
                            qf = self.qt[w]
                            ni = len(self.index[(w,)])
                            bm25score += log(((RI+.5)/(R-RI+.5))/((ni-RI+.5)/(self.N-ni-R+RI+.5))*((K1+1)*tf)/(K+tf)*((K2+1)*qf)/(K2+qf))
                            break
        return(bm25score)

    def search(self, ID, query):
        query = query.casefold()
        self.qt = Counter(query.split())
        ranking = []
        for file in self.length:
            ranking.append((file, self.computeBM25(file, query)))
        ranking.sort(key=lambda x: x[1], reverse=True)
        df = pandas.DataFrame(ranking[:100],columns=["File","BM25 Score"])
        df.insert(0, 'ID', ID)
        df.insert(1, 'Q', 'Q0')
        df.insert(4, 'System Name',SYSTEM_NAME)
        print(df)
        if not os.path.exists("Task1-Rankings"):
            os.mkdir("Task1-Rankings")
        with open("Task1-Rankings/"+ query + ".txt", "w+") as fout:
            fout.write(df.to_string())
        print(str(ID) + " " + query + "\t Rankings Saved")

if __name__ == "__main__":
    corpusdir = str(input("Input the Name / dir path for the corpus folder: "))
    indexFile = str(input("Input the Name / dir path for index txt file: "))
    print("Processing .......")
    bm = BM25(corpusdir,indexFile)

    choice = str(input("Type 1 to use *Querylist* file to get rankings for all 5 queries at once or type 2 to input individual (Id + Query) for ranking : "))
    if choice == "1" :    # letting the user choose to either give a list of queries or enter them one by one.
        with open("querylist" + ".txt", "r") as fout:
            ID = 0
            for line in fout:
                ID += 1
                line = line.strip("\n")  # removing newlines
                bm.search(ID, line)
    elif choice == "2":
        while True:
            ID = input("Enter Query ID (Enter Q/q to exit): ")
            if ID.casefold() == 'q':
                break
            query = str(input("Enter Query Text: "))
            bm.search(ID, query)

    else:
        print("Error: Invalid Selection")
