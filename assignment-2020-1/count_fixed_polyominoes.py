from pprint import pprint
import sys
def zeroing_array(x,y):
    arr=[]
    for i in range(x):
        arr_t=[0 for _ in range(y)]
        arr.append(arr_t)
    return arr
def graph_constractor(n):
    adjList = {}
    if n>1:#if n=1 the graph={}
        graph=zeroing_array(2*n-2,n) #zeroing the array
        #building the right of the graph
        for x in range(0,n):
            for y in range(n-x-1,-1,-1):
                graph[x+n-2][y]=1#add a node in the array
        #building the left of the graph
        for x in range(2-n,0):
            for y in range(2-n,x+1):
                graph[x+n-2][y+n-1]=1 #add a node in the array
        #filling adjList
        for x in range(2*n-2):
            for y in range(n):
                if graph[x][y]==1: #is a node
                    #finding neighbors
                    key=(x-n+2,y)
                    adjList[key]=[]
                    if x!=2*n-3: #checking if we are at the and of the table
                        if graph[x+1][y]==1: #checking right
                            right=(x-n+3,y)
                            adjList[key].append(right)
                    if y!=n-1: #checking if we are at the and of the table
                        if graph[x][y+1]==1: #checking up
                            up=(x-n+2,y+1)
                            adjList[key].append(up)
                    if x!=0: #checking if we are at the and of the table
                        if graph[x-1][y]==1: #checking left
                            left=(x-n+1,y)
                            adjList[key].append(left)
                    if y!=0: #checking if we are at the and of the table
                        if graph[x][y-1]==1: #checking down
                            down=(x-n+2,y-1)
                            adjList[key].append(down)
    return adjList
def count_fixed_polyominoes(g,untried,n,p,c):
    while untried: #while the untried list is not emptry
        u=untried.pop() #remove from untried and add to u
        p.append(u)#check
        if len(p)==n:
            c.add()
        else:
            new_neighbors=set()
            for v in g[u]:
                if not(v in untried) and not(v in p) and not(are_there_neighbors(g,v,p,u)):
                    new_neighbors.add(v)
            new_untried=new_neighbors|untried #union of the sets
            count_fixed_polyominoes(g,new_untried,n,p,c)
        p.remove(u)
    return c.valueOf()
class Count:
    def __init__(self):
        self.c=0
    def add(self):
        self.c+=1
    def valueOf(self):
        return self.c
def are_there_neighbors(g,v,p,u): #checks the trird requirment
    there_are=False
    for node in p:
        if node!=u:
            for neighbor in g[node]:
                if v==neighbor:
                    there_are=True
    return there_are
counter=Count()
if len(sys.argv)==2:
    print(count_fixed_polyominoes(graph_constractor(int(sys.argv[1])),{(0,0)},int(sys.argv[1]),[],counter))
else:#gives -p
    if sys.argv[1]=='-p':
        pprint(graph_constractor(int(sys.argv[2])))
    print(count_fixed_polyominoes(graph_constractor(int(sys.argv[2])),{(0,0)},int(sys.argv[2]),[],counter))
