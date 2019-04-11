from collections import defaultdict

WIKI = "https://en.wikipedia.org/wiki/"       # for concatenating with docID


class PageRanker(object):

    def readGraph(self, inputFilename):
        self.inLinks = defaultdict(list)
        self.outCount = defaultdict(int)
        self.inCount = defaultdict(int)
        with open(inputFilename, 'r') as inputFile:
            for line in inputFile:
                docs = line.rstrip('\n').split(' ')
                doc, inLinks = docs[0], docs[1:]
                for inLink in inLinks:
                    self.inLinks[doc].append(inLink)
                    self.inCount[doc] += 1
                    self.outCount[inLink] += 1
        self.docs = self.inLinks.keys()
        self.N = len(self.docs)
        self.sources = [doc for doc in self.docs if self.inCount[doc] == 0]
        self.sinks = [doc for doc in self.docs if self.outCount[doc] == 0]

        print("Sources",self.sources)
        print("Sinks",self.sinks)
        print(max(self.inCount.values()))
        print(max(self.outCount.values()))


        with open(inputFilename + " Statistics.txt", 'w+') as fout:
            fout.write("Sources \n")
            fout.write(str(self.sources))
            fout.write("\nSinks \n")
            fout.write(str(self.sinks))
            fout.write("\nMax In-Degree \n")
            fout.write(str(max(self.inCount.values())))
            fout.write("\nMax Out-Degree\n")
            fout.write(str(max(self.outCount.values())))
        return self.inLinks

    def getl2Norm(self, pr):
        l2 = 0.0
        for doc in self.docs:
            p = pr[doc]
            l2 += p**2
        return l2 ** 0.5

    def converged(self, pr):
        self.l2Norm.append(self.getl2Norm(pr))
        self.pr_iter.append(pr)
        l = len(self.l2Norm)
        if l < 5:
            return False
        for i in range(l - 4, l):
            if abs(self.l2Norm[i] - self.l2Norm[i - 1]) >= 0.0005:
                return False
        return True

    def compute(self, d=0.85, maxIter=None):
        self.l2Norm = []
        self.pr_iter = []
        pr = defaultdict(int)
        for doc in self.docs:
            pr[doc] = 1.0 / self.N
        while not self.converged(pr):
            if maxIter and len(self.l2Norm) > maxIter:
                break
            newPR = defaultdict(int)
            sinkPR = 0
            for doc in self.sinks:
                sinkPR += pr[doc]
            for doc in self.docs:
                newPR[doc] = (1 - d) / self.N
                newPR[doc] += d * sinkPR / self.N
                for inLink in self.inLinks[doc]:
                    newPR[doc] += d * pr[inLink] / self.outCount[inLink]
            pr = newPR
        self.pr = pr
        return pr

    def outputTopK(self, k, filename):
        result = sorted(self.pr.items(), key=lambda x: -x[1])[:k]
        with open(filename, 'w+') as fout:
            fout.write("Rank"+"\t\t"+"Page(Prefix + docID)" +"\n")
            for docID, pr in result:
                fout.write(str(pr) + "\t" + WIKI+docID + '\n')

    def outputl2Norm(self, filename):
        with open(filename, 'w+') as fout:
            fout.write("L2-Norm"+"\t\t\t"+"Total PR" +"\n")
            for l in range(len(self.l2Norm)):
                fout.write(str(self.l2Norm[l]) +"\t"+ str(sum(self.pr_iter[l].values()))+ '\n')

    def rankByInLinkCount(self):
        self.pr = {}
        for doc in self.docs:
            self.pr[doc] = len(self.inLinks[doc])


if __name__ == "__main__":
    pr = PageRanker()
    inputFilename = input("Enter the graph filename (*.txt): ")
    pr.readGraph(inputFilename)

    # Run one of the following lines to get the desired asnwer from Task 4,
    # comment out the others

    pr.compute()                 # baseline: d = 0.85 ie. Lambda = 0.15
    #pr.compute(d=.75)           # for Lambda = 0.25 i.e d = 0.75
    #pr.compute(d=.65)           # for Lambda = 0.35 i.e d = 0.65
    #pr.compute(d=.5)            # for Lambda = 0.5 i.e d = 0.5
    #pr.compute(maxIter=4)       # iteration = 4
    #pr.rankByInLinkCount()      # rank by in-link count

    k = int(input("Enter top k results to output: k = "))
    rankingFile = input("Enter the ranking output filename [with.txt suffix]: ")
    pr.outputTopK(k, rankingFile)

    if hasattr(pr, "l2Norm"):
        l2NormFile = input("Enter the L2Norm output filename [with.txt suffix]: ")
        pr.outputl2Norm(l2NormFile)
