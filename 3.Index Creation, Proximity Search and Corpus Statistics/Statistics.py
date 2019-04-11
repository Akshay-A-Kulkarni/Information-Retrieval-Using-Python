import math
import os

if not os.path.exists("statistics"):
    os.mkdir("statistics")


nrange = int(input("Enter the value of n entered previously : n = "))

for n in range(1,nrange+1):
    file = "indexes/freq" + str(n) + ".txt"
    with open(file, 'r') as filein:
        index = ast.literal_eval(filein.read())  #loading from disk
    tf, df = {}, {}
    for term, records in index.items():
        df[term] = len(records)
        count = 0
        for doc, cnt in records:
            count += cnt
        tf[term] = count


    with open("statistics/termFreq" + str(n) + ".txt", "w+") as fout: #  creating tf and df tables
        tf = sorted(tf.items(), key=lambda x: x[1], reverse=True)  # sorting the items from dict
        for term, freq in tf:
            fout.write(str(term) + ":\t" + str(freq) + '\n')
    with open("statistics/docFreq" + str(n) + ".txt", "w+") as fout:
        df = sorted(df.items())
        for term, freq in df:
            fout.write(str(term) + ":\t" + str(freq) + '\n')
            for doc, cnt in index[term]:
                fout.write(doc + '\n')

    # Generate stoplist
    with open("statistics/stoplist" + str(n) + ".txt", "w+") as fout:
        for term, freq in df.items():
            if freq > 600:
                fout.write(str(term) + ':\t' + str(freq) + '\n')
