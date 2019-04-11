import nltk as nltk
nltk.download('punkt')  # updating punkt
nltk.download('stopwords') #updating stopwords list.
from nltk.corpus import stopwords
from nltk import ngrams
import os
from collections import OrderedDict



def getInvertedIndexes(lines,stops):

    invertedIndex = {}
    # Getting data from text file and adding their relevant positions.
    for l in lines:
        file_name = l.rsplit('\\', 1)[-1]
        file_name.replace("'","%27")
        name_file = "corpus/" + file_name
        with open(name_file.strip(), encoding='utf8') as file_text_data:
            file_content = file_text_data.read()
            token = nltk.word_tokenize(file_content)
            filtered_words = [word for word in token if word not in stops]
            generated = ngrams(filtered_words, 1)
        unigrams = createDictionary(generated) # creating a dictionary of unigrams
        invertedIndex = createInvertedIndex(invertedIndex, file_name.strip(), unigrams)
    return invertedIndex


def createInvertedIndex(invertedIndex,textFileName, unigrams):

    for gen, value in unigrams.items():
        try:
            invertedIndex[gen].append((textFileName, unigrams[gen]))
        except KeyError:
            invertedIndex[gen] = [(textFileName, unigrams[gen])]
    return invertedIndex


def createDictionary(gen):

    unigrams= {}

    for g in gen:
        if g in unigrams:
            unigrams[g] = unigrams[g] + 1
        else:
            unigrams[g] = 1
    return unigrams


def getTermFreq(k_val):

    out_files = os.listdir("lucene_search_results")
    stops = set(stopwords.words('english'))
    stops.add("edit")
    for file in out_files:
        with open("lucene_search_results/" + file, encoding="utf8") as file_data:
            lines = []
            for d in range(k_val): # taking top k documents
                lines.append(file_data.readline())
            inverted_index = getInvertedIndexes(lines,stops)
            sorted_term_freq = TermFreq(inverted_index)
            save_terms_file(k_val, file,sorted_term_freq)
            create_Expansion_Terms(k_val,sorted_term_freq,file)


def TermFreq(inverted_index):

    termFrequency = {}
    for term, doc_ids in inverted_index.items():
        count = 0
        for i, j in doc_ids:
            count = count + j
        termFrequency[term] = count
    sorted_term_freq = OrderedDict((k, v) for k, v in sorted(termFrequency.items(), key=lambda x: x[1], reverse=True))
    return sorted_term_freq


def save_terms_file(k_val,n, term_freq):
    newpath = os.getcwd()+"\\Term_Frequencies"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    with open("Term_Frequencies/termFrequency"+ "_k-"+str(k_val)+"_"+ str(n), 'w', encoding="utf-8") as file_data:
        for key,value in term_freq.items():
            file_data.write(str(key[0]) + " ")
            file_data.write(": " + str(value) + "\n")
    file_data.close()

def create_Expansion_Terms(k_val,term_freq,file): #creating expanded query file
    n=[8,7,6]
    with open("QueryExpansionTerms", 'a', encoding="utf-8") as file_data:
        file_data.write("The expansion terms for Query : "+ str(file[:-4])+"\n")
        file_data.write(" "+ "\n")
        for i in n:
            file_data.write("For k = "+str(k_val) +" And "+"n= "+ str(i)+"\n")
            file_data.write(str(list(term_freq.keys())[0:i])+"\n"+"\n")
    file_data.close()



if __name__ == '__main__':
    # Set K-values.
    k_val = 15
    #k_val = 10
    #k_val = 15
    getTermFreq(k_val) # Writes the term frequencies in descending order.
