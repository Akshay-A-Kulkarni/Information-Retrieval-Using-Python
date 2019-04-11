from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import re
import requests

WiKi = "https://en.wikipedia.org" # Prefix for the links extracted.


class WikiCrawler(object):             # Inheriting from object for compatibility

    def __init__(self, seedURL, depth = 6, wait = 1, max = 1000, keywords=None):
        self.seedURL = seedURL         # input URL
        self.depth = depth             # Depth crawl limit
        self.wait = wait               # Delay between each GET request in secs
        self.max = max                 # Maximum no. of links to crawl
        self.keywords = keywords       # Keywords for focused crawl

    def scrapeLinks(self, url):
        sleep(self.wait)
        # Introducing one sec delay to crawler to adhere to politeness policy
        req = requests.get(url)
        if req.status_code != requests.codes.ok or req.is_redirect:
            return[]
        # Checking against the built-in status code lookup object for easy-
        # -reference to see if a valid response was received from wiki

        body_content = BeautifulSoup(req.content,'lxml').find(id="bodyContent")
        # Using BeautifulSoup to parse the requested response object
        links = []
        for anchor in body_content.find_all("a"):
            link = anchor.get("href")
            if link and re.match("/wiki/.*", link) is not None \
                    and re.match('/wiki/Main_Page', link) is None \
                    and re.match('/wiki/(.*)#(.*)', link) is None \
                    and re.match('/wiki/(.*):(.*)', link) is None:
                    if self.keywords is not None \
                                    and not self.hasKeyword(link, anchor.string):
                        continue
                    #print(WiKi+link)
                    links.append(WiKi+link)
        return links


    def hasKeyword(self, url, text):
        self.keywords = [word.lower() for word in keywords]if keywords else None
        for word in self.keywords:
            if url.lower().find(word) != -1 \
               or(text and text.lower().find(word) != 1):
                return True
        return False



    def BFS(self):
        self.result = [self.seedURL]
        depth = {self.seedURL:1}
        num_links = 1
        self.dup_count = 0
        for url in self.result:
            if depth[url] > self.depth:  # limiting depth
                print("Maximum depth hit : Depth = ", self.depth)
                return
            links = self.scrapeLinks(url)
            for link in links:
                if link in depth:
                    self.dup_count += 1     # tracking suplicate urls
                else:
                    depth[link] = depth[url] + 1
                    self.result.append(link)
                    num_links += 1          #keeping count
                    if num_links >= self.max:
                        print("Max URL crawl cap reached: Depth touched = ", depth[link])
                        return

    def DFS(self):
        self.result = []
        self.visited = {self.seedURL:True}          # Creating a dict
        self.maxdepth = 1                           # Initialising maxdepth
        self.dfs_imp(self.seedURL, 1)
        print("Max Depth reached: ", self.maxdepth)

    def dfs_imp(self, url, depth):
        self.maxdepth = max(depth , self.maxdepth)
        self.result.append(url)
        self.visited[url] = True
        if len(self.result) >= self.max:        # limiting no of urls to 1000
            return
        if depth < self.depth:
            for link in self.scrapeLinks(url):
                if len(self.result) < self.max and link not in self.visited:
                    self.dfs_imp(link, depth + 1)

    def writeFile(self, filename):              # saving results to txt file
        file = open(filename, "w")
        for link in self.result:
            file.write(link + "\n")
        file.close()

    def saveFile(self, filename):
        with open (filename, "w") as file:
            for link in self.result:
                file.write(link + "\n")



if __name__ == "__main__":
    seedURL = input("Please enter a seed URL: ")
    keywords = input("Please enter keywords for focused crawling (separated by a single space): ").split(' ')

    crawler = WikiCrawler(seedURL)

    file_time = datetime.now().strftime("(%Y-%m-%d)")      #retrieving date and time of run as a string
    x1= file_time
    file_format = ".txt"

    print("Task1 Breadth-First Search:")
    crawler.BFS()
    crawler.saveFile("Task1_BFS" + file_time + file_format)

    print("Task1 Depth-First Search:")
    crawler.DFS()
    crawler.saveFile("Task1_DFS"+ file_time + file_format)

    print("Task2 Focused Breadth-First Search:")
    focusedCrawler = WikiCrawler(seedURL, keywords=keywords)
    focusedCrawler.BFS()
    focusedCrawler.saveFile("Task2_FBFS"+ file_time + file_format)

    print("Focused Crawl duplicate URLs = " , focusedCrawler.dup_count)

    FBFS_file = "Task2_FBFS"+ file_time + file_format

    with open (FBFS_file, "a") as file: # append in the text file
        file.write("The number of duplicate URLs in focused crawl was {}".format(focusedCrawler.dup_count))
