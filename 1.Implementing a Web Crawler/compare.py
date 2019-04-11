from datetime import datetime
file_format = ".txt"
file_date = datetime.now().strftime("(%Y-%m-%d)")
hash = {}
bfs = open("Task1_BFS" + file_date + file_format, 'r')
dfs = open("Task1_DFS" + file_date + file_format, 'r')

for link in bfs:
    hash[link] = True

count = 0
for link in dfs:
    if link in hash:
        count += 1

print("the URL overlap is" ,count)

bfs.close()
bfs.close()
