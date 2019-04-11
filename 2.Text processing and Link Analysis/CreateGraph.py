import collections, requests, re
from time import sleep
from bs4 import BeautifulSoup

class createGraph(object):
    def __init__(self, inputFile,inputFolder):

        with open(inputFile, 'r') as fin:
            self.docs = set([line[30:].rstrip('\n') for line in fin.readlines()])
        self.graph = collections.defaultdict(list)

    def getLinks(self, docID):
        #sleep(1)
        title = docID
        if title.find("/") != -1 :       # to handle invalid filnames in links as we've stored them
            title = title.replace("/","_")
        with open("./"+inputFolder+"/" + title + ".txt", 'r', encoding='utf8') as fout:
            filesoup = BeautifulSoup(fout,'html.parser')

        body = filesoup.find(id="bodyContent")
        links = set()
        for href in body.find_all("a"):
            link = href.get("href")
            if link and re.match('/wiki/.*', link) is not None \
                    and re.match('/wiki/Main_Page', link) is None \
                    and re.match('/wiki/(.*)#(.*)', link) is None \
                    and re.match('/wiki/(.*):(.*)', link) is None \
                    and link[6:] in self.docs:
                links.add(link[6:])
        return links

    def build(self):
        for docID in self.docs:
            for link in self.getLinks(docID):
                if link != docID:
                    self.graph[link].append(docID)

    def output(self, filename):
        with open(filename, 'w+') as file:
            for doc, inLinks in self.graph.items():
                file.write(doc)
                for inLink in inLinks:
                    file.write(' ' + inLink)
                file.write('\n')


if __name__ == "__main__":
    inputFile = input("Enter the filename containing wiki page links: ")
    inputFolder = input("Enter the folder containing wiki pages: ")
    cg = createGraph(inputFile , inputFolder)
    cg.build()
    outputFile = input("Enter the output filename: ")
    cg.output(outputFile)
