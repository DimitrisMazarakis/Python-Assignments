from collections import deque 
import sys
def graphs(file,deleted_node):#methodos gia to proairetiko meros
    from graphviz import Graph
    dot = Graph(node_attr={'color': 'lightblue2', 'style': 'filled'},format='jpg',engine='fdp')
    visited={}
    adjList=create_graph(file)
    deleted=False
    for x in adjList:
        visited[x]=False
    for key in adjList:
        for erased in deleted_node:
            if key==erased:
                dot.node(str(key),str(key),color='lightgrey')
                deleted=True
        if not deleted:
            dot.node(str(key),str(key))
        deleted=False
        for i in adjList[key]:
            if not visited[i]:
                for erased in deleted_node:#elegxei an exoun diagraftei oi komvoi i kai key
                    if erased==i or erased==key:
                        deleted=True
                if not deleted:#den exoun diagraftei ara tous enono
                    dot.edge(str(key),str(i))
                deleted=False
            visited[key]=True
    dot.view()
def create_graph(file):
    g = {}
    with open(file) as graph_input:
        for line in graph_input:
            nodes = [int(x) for x in line.split()]
            if len(nodes) != 2:
                continue
            if nodes[0] not in g:
                g[nodes[0]] = []
            if nodes[1] not in g:
                g[nodes[1]] = []
            g[nodes[0]].append(nodes[1])
            g[nodes[1]].append(nodes[0])
    return g
def algo_1(adjList,deleted,file,deleted_nodes,proeretiko):
    if deleted>0:
        degrees=find_degree(adjList)
        max_node=find_max_node(degrees)#upologizei poios komvos prepei na diagraftei
        if proeretiko:
            graphs(file,deleted_nodes)#emfanizei ton neo grafo
        delete_node(max_node,adjList,degrees)
        del adjList[max_node]
        deleted_nodes.append(max_node)
        algo_1(adjList,deleted-1,file,deleted_nodes,proeretiko)
def find_max_node(array):
    max_array=-1
    max_node=-1
    for node in array:
        if array[node]>max_array:
            max_array=array[node]
            max_node=node
        elif array[node]==max_array:
            if node<max_node:
                max_array=array[node]
                max_node=node
    return max_node
def find_degree(adjList):#finds the degree of each node in the graph
    degrees={}
    for node in adjList:
        degrees[node]=len(adjList[node])
    return degrees
def delete_node(max_node,adjList,degree_or_influence):
    print(max_node,degree_or_influence[max_node])
    for key in adjList:
        exists=False
        spot_to_delete=0
        for node in range(len(adjList[key])):
            if adjList[key][node]==max_node:
                exists=True
                spot_to_delete=node
        if exists:
            del adjList[key][spot_to_delete]
def algo_2(adjList,r,deleted,file,deleted_nodes,proeretiko):
    if deleted>0:
        top_influence={}
        degrees=find_degree(adjList)
        for node in adjList:
            top_influence[node]=(degrees[node]-1)*bfs(adjList,degrees,node,r)
        max_spot=find_max_node(top_influence)#upologizei poios komvos prepei na diagraftei
        if proeretiko:
            graphs(file,deleted_nodes)#emfanizei ton neo grafo
        delete_node(max_spot,adjList,top_influence)
        top_influence=update_top_influence2(adjList,top_influence,r,max_spot)
        del adjList[max_spot]
        deleted_nodes.append(max_spot)
        algo_2(adjList,r,deleted-1,file,deleted_nodes,proeretiko)
def update_top_influence2(adjList,top_influence,r,node):
    q = deque()
    degrees=find_degree(adjList)
    visited={}
    inqueue={}
    for x in adjList:
        visited[x]=False
        inqueue[x]=False
    q.appendleft(node)
    inqueue[node] = True
    layer=[]
    layer.extend(adjList[node])
    r_adj=1
    while not (len(q) == 0):
        c = q.pop()
        inqueue[c] = False
        visited[c] = True
        if c!=node and not (c in layer):
            r_adj+=1
            temp=[]
            for i in layer:
                    temp.extend(adjList[i])
            layer=temp
        if r_adj<r+1:
            top_influence[c]=(degrees[c]-1)*bfs(adjList,degrees,c,r)
        elif r_adj==r+1:
            return top_influence
        for v in adjList[c]:
            if not visited[v] and not inqueue[v]:
                q.appendleft(v)
                inqueue[v] = True
    return top_influence
def bfs(adjList,degrees,node,r):
    sum=0
    q = deque()
    visited={}
    inqueue={}
    for x in adjList:
        visited[x]=False
        inqueue[x]=False
    q.appendleft(node)
    inqueue[node] = True
    layer=[]
    layer.extend(adjList[node])
    r_adj=1
    while not (len(q) == 0):
        c = q.pop()
        inqueue[c] = False
        visited[c] = True
        if c!=node and not (c in layer):
            r_adj+=1
            temp=[]
            for i in layer:
                temp.extend(adjList[i])
            layer=temp
        if c!=node and r_adj==r:
            sum+=degrees[c]-1
        elif r_adj>r:
            return sum
        for v in adjList[c]:
            if not visited[v] and not inqueue[v]:
                q.appendleft(v)
                inqueue[v] = True
    return sum
deleted_nodes=[]
if sys.argv[1]=='-c':
    if '-t' in sys.argv:#proeretiko kommati
        algo_1(create_graph(sys.argv[3]),int(sys.argv[2]),sys.argv[3],deleted_nodes,True)
    else:
        algo_1(create_graph(sys.argv[3]),int(sys.argv[2]),sys.argv[3],deleted_nodes,False)
elif sys.argv[1]=='-r':
    if '-t' in sys.argv:#proeretiko kommati
        algo_2(create_graph(sys.argv[4]),int(sys.argv[2]),int(sys.argv[3]),sys.argv[4],deleted_nodes,True)
    else:
        algo_2(create_graph(sys.argv[4]),int(sys.argv[2]),int(sys.argv[3]),sys.argv[4],deleted_nodes,False)
