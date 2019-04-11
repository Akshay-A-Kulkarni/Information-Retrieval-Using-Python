import os
import glob
from time import sleep
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
import string
import pandas
import matplotlib.pyplot as plt


class parseAndTokenize(object):

    def parseHtmlFile(self,inputfile,inputFolder):

        filesoup = BeautifulSoup(inputfile,'html.parser') #loading the input file as a soup object

        soup = filesoup.find(id = "mw-content-text")

        [s.decompose() for s in soup('table')]
        [s.decompose() for s in soup('style')]
        [s.decompose() for s in soup.find_all(id ='toc')]
        [s.decompose() for s in soup.find_all(class_="hatnote navigation-not-searchable")]
        [s.decompose() for s in soup.find_all(class_="thumb tright")]
        [s.decompose() for s in soup.find_all(class_="thumb tleft")]
        [s.decompose() for s in soup.find_all(class_="thumb tmulti tright")]
        [s.decompose() for s in soup.find_all(class_="thumb tmulti tleft")]
        [s.decompose() for s in soup.find_all(class_="mw-editsection")]
        [s.decompose() for s in soup.find_all(class_="mwe-math-element")]
        [s.decompose() for s in soup.find_all(class_="reflist")]

        file_title = filesoup.title.string
        invalid_chars = """<>:"/\|?*"""
        for c in invalid_chars:
            if file_title.find(c) != -1 :                       # to handle invalid filnames in links
                file_title = file_title.replace(c,"_")

        if inputFolder =="htmls":
            if not os.path.exists("./htmls_parsed_text"):     #generates a folder if one doesnt exist.
                os.makedirs("./htmls_parsed_text")
        elif not os.path.exists("./fhtmls_parsed_text"):
                    os.makedirs("./fhtmls_parsed_text")


        with open("./" + inputFolder + "_parsed_text/"+ file_title +".txt", 'w+', encoding='utf8') as fout:
                fout.write(filesoup.title.string)
                fout.write(soup.get_text())


    def readAndParseAllFiles(self):

        inputFolder = input("Enter the input folder containing wiki articles to be cleaned: ")
        file_list = glob.glob(os.path.join(os.getcwd(), inputFolder, "*.txt"))
        for input_file in file_list:
            with open(input_file, "r",encoding = "utf8") as fin:
                self.parseHtmlFile(fin,inputFolder)

    def caseFolding(self,input_list):
        return [word.casefold() for word in input_list] #case fold handling

    def handlePunctuations(self,input_list):
        punct_list = string.punctuation
        punct_list = list("""!"#$%&''()*+,./:;<=>?@[\]^_`{|}~ """)
        stripped = []
        for word in input_list:
            if word not in punct_list:
                stripped.append(word)
            else: None
        return stripped

    def tokenizeTrigramsAndPlot(self):
        #inputFolder = input("Enter the input folder containing wiki articles to be tokenized ie parsed articles: ")
        # ie parsed_text
        file_list = glob.glob(os.path.join(os.getcwd(), "htmls_parsed_text", "*.txt"))
        corpus = []
        complete_corpus_trigrams = []

        for file_path in file_list:
            with open(file_path,encoding="utf8") as f_input:
                corpus.append(f_input.read())

        for item in corpus:
            tokenized_words = word_tokenize(item)
            tokenized_words = self.caseFolding(tokenized_words)
            tokenized_words = self.handlePunctuations(tokenized_words)
            #Create your Trigrams
            tgs = nltk.trigrams(tokenized_words)
            for values in tgs:
                complete_corpus_trigrams.append(values)
        #compute frequency distribution for all the trigrams in the text
        fdist = nltk.FreqDist(complete_corpus_trigrams)
        complete_tgs_freq = []

        for k,v in fdist.items():
            complete_tgs_freq.append([k,v])

        comp_tgs_by_freq = sorted(complete_tgs_freq, key=lambda x: x[1], reverse=True) # sort in descending order.
        comp_tgs_freq_rank = []   # Final list of lists containing trigram|freq|rank
        r=1
        for l in comp_tgs_by_freq :
            l.append(r)
            r += 1
            comp_tgs_freq_rank.append(l)
        # Saving file to a dataframe
        corpus_tgs_df = pandas.DataFrame(comp_tgs_freq_rank)
        corpus_tgs_df.columns = ['Trigram','Frequency','Rank']
        print(corpus_tgs_df[:10])
        corpus_tgs_df.to_csv("Corpus_Trigrams_Data.txt", encoding='utf-8')
        corpus_tgs_df[:50].to_csv("Corpus_Trigrams_Data(Top 50).tsv", sep= "\t",encoding='utf-8')
        # For plotting
        freq = [item[1] for item in comp_tgs_freq_rank]
        rank = [item[2] for item in comp_tgs_freq_rank]

        size = corpus_tgs_df.size

        print("-------------")
        print("Size = ",size)

        prob = [item[1]/size for item in comp_tgs_freq_rank]

        c = [rank[i]*prob[i] for i in range(len(rank))]

        avg_c = sum(c) / float(len(c))

        print("The Trigram frequency as shown by graph, obeys Zipf's Law, Therefore")
        print("The constant corresponding to Pr * r =",avg_c)


        plt.figure()
        plt.loglog(rank,freq,"bs",markersize=6)
        plt.title('Freq vs Rank')

        plt.figure()
        plt.loglog(rank,prob,"g^",markersize=6)
        plt.title('Prob vs Rank')
        #plt.xscale('log')
        #plt.yscale('log')
        plt.figure()
        plt.grid(True)
        plt.savefig('Task1_Zipf.png')



if __name__ == "__main__":

    pnt = parseAndTokenize()
    # Un/comment each or both to get the respective cleaned text and tokens
    #pnt.readAndParseAllFiles()
    pnt.tokenizeTrigramsAndPlot()
