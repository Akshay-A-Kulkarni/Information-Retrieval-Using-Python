import os, requests
from time import sleep

inputFile = input("Enter the input filename containing wiki links: ")
fin = open(inputFile, 'r')


if inputFile == "BFS.txt":
    foldername = "htmls"
else:
    foldername = "fhtmls"

if not os.path.exists("./" + foldername):
    os.makedirs("./" + foldername)


for link in fin:
    sleep(1)
    link = link.rstrip('\n')
    title = link[30:]
    if title.find("/") != -1 :       # to handle invalid filnames in links
        title = title.replace("/","_")

    with open("./" + foldername + "/" + title + ".txt", 'w+', encoding='utf8') as fout:
        fout.write(requests.get(link).text)

fin.close()
