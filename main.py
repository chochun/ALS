from pygraphml import Graph
from pygraphml import GraphMLParser
import numpy as np
import optimizer as opt
import itertools
import greedy as gd
import operator
import plotgraph as plg
import CKR 

def getNodes(weights):
    nodes = []
    for e, w in weights.items():
        if e.node1 not in nodes:
            nodes.append(e.node1)
        if e.node2 not in nodes:
            nodes.append(e.node2)
    return nodes
def getEdges(weights):
    edges = []
    for e, w in weights.items():
        if e not in edges:
            edges.append(e)
    return edges

def getAdjNodes(node):
    nodes = []
    for e in node.edges():
        if e.node1 != node:
            nodes.append(e.node1)
        if e.node2 != node:
            nodes.append(e.node2)
    return nodes

def DFS(u, t, visited, path, paths):
    visited[u.id] = True
    path.append(u)
    if u == t:
        paths.append(path[:])
    else:
        for n in getAdjNodes(u):
            if not visited[n.id]:
                DFS(n, t, visited, path, paths)
    path.pop()
    visited[u.id] = False    

def getAllPathsByNode(s, t, g):
    paths = []
    path = []
    visited = {}
    for n in g.nodes():
        visited[n.id] = False
    DFS(s, t, visited, path, paths)
    return paths

def pathThrCount(paths):
    count = {}
    for p in paths:
        for e in p:
            count[e] = count.get(e, 0) + 1
    return count
    
def getPathsByEdge(s, t, g, amoutPath=float("inf")):
    pathsN = []
    pathsE = []
    path = []
    visited = {}
    for n in g.nodes():
        visited[n.id] = False
    DFS(s, t, visited, path, pathsN)
    for pN in pathsN:
        pE = []
        for i in range(len(pN) - 1):
            end1 = pN[i]
            end2 = pN[i+1]
            for e in end1.edges():
                if (e.node1==end1 and e.node2==end2) or (e.node1==end2 and e.node2==end1):
                    pE.append(e)
        pathsE.append(pE)
        if len(pathsE) >amoutPath:
            break
    return pathsE

def placeMonitors(g, amount):        
    monitors = []  
    #selectedNodes = [0,5]
    selectedNodes = np.random.choice(len(g.nodes()), amount, replace=False)
    for n in g.nodes():
        #put the monitors to the points which are connected by a single link.
        #if len(n.edges()) == 1:
        if int(n.id) in selectedNodes:
            monitors.append(n)
    return monitors

def showPathsByNode(paths):
    for path in paths:
        pstring = "-"
        for n in path:
            pstring = pstring + n.id + "-"
        print(pstring)

def showPathsByEdge(paths, edgesLabel):
    for path in paths:
        pstring = "-"
        for e in path:
            pstring = pstring + str(edgesLabel[e]) + "-"
        print(pstring)
def getArr(paths, edgesLabel):
    nLinks = len(edgesLabel)
    arr = np.zeros((len(paths), nLinks))
    for i in range(len(paths)):
        for e in paths[i]:
            j = edgesLabel[e]
            arr[i,j] = 1
    return arr

def isHitAll(edges, paths, labelEdge):
    isPathHit = {}
    for i in range(len(paths)):
        isPathHit[i] = False
    for e in edges:
        eadd = labelEdge[e]
        for i in range(len(paths)):
            if eadd in paths[i]:
                isPathHit[i] = True
    return all(isPathHit.values())

def getAllHitRes(paths, labelEdge, results):
    minall = float('inf')
    allHit = []
    maxnonall = 0
    nonAllHit = []
    for r in results:
        val = r[0]
        edges = r[2]
        if isHitAll(edges, paths, labelEdge):
            allHit.append(r)
            minall = min(val, minall)
        else:
            nonAllHit.append(r)   
            maxnonall = max(val, maxnonall)
    return allHit, minall, nonAllHit, maxnonall
def topTraversal(percentile, weight):
    lm = []
    number = int(np.ceil((percentile/100)*len(weight)))
    sortedLinkByTraveral = sorted(weight.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(number):
        lm.append(sortedLinkByTraveral[i][0])
    return lm

def getMinTra(edgesLabel, lm, paths, t, tmax, x0):
    pm = []
    pn = []
    
    #given lm, create array for pn,pm
    for path in paths:
        isNormal = True
        for e in path:
            if e in lm:
                isNormal = False
                pm.append(path)
                break
        if isNormal:
            pn.append(path)            
    rm = getArr(pm, edgesLabel)
    rn = getArr(pn, edgesLabel)
    res = opt.maxdam(rn, rm, lm, t, tmax, x0, edgesLabel)
    return res

def getWeight(paths):
    weights={}
    for path in paths:
        for e in path:
            weights[e] = weights.get(e, 0) + 1
    return weights

if __name__ == "__main__":
    #set up initial value:t, tmax
    t = 5
    tmax = 11
    allres = []
    alllm = []
    #get the graph
    parser = GraphMLParser()
    #g = parser.parse("./archive/AttMpls.graphml")
    g = parser.parse("./archive/AttMpls.graphml")
    #g.show()
    #monitors, and then get paths
    #numberMonitor = 3
    #numberPathsBtw2M = 5
    #monitors = placeMonitors(g, numberMonitor)
    numberMonitor = 5
    numberPathsBtw2M = float('inf')
    monitors = placeMonitors(g, numberMonitor)
    allpaths = []
    for i in range(len(monitors)):
        for j in range(i+1, len(monitors)):
            allpaths += getPathsByEdge(monitors[i], monitors[j], g, numberPathsBtw2M)
    paths = allpaths
    print("paths are defined")
    print("# of paths:{}".format(len(paths)))
    #establish label for edges
    #This is the order of vector x
    #For example: x=[ea, ec, eb] => edgesLabel[ea]=0, edgesLabel[eb]=2, edgesLabel[ec]=1,
    edgesLabel = {}
    i = 0
    for e in g.edges():
        edgesLabel[e] = i
        i+=1
    
    labelEdge = {}
    for edge, l in edgesLabel.items():
        labelEdge[l] = edge
    
    #set up x0 (initial value)
    x0 = np.zeros(len(edgesLabel))
    #for i in range(x0.size):
    #    x0[i] = t
    
    weights = getWeight(paths)
    nodes = getNodes(weights)
    edges = getEdges(weights)
    print("# of nodes:{}".format(len(nodes)))
    print("# of edges:{}".format(len(edges)))
    #create Lm
    print("greedy")
    lm = gd.greedy(weights, paths)
    #print("Lm:{}".format(lm))
    res = getMinTra(edgesLabel, lm, paths, t, tmax, x0)        
    #print("result:{}".format(res))
    pos=plg.plot(g, weights, monitors, lm)
    allres.append(res[0])
    alllm.append(len(lm))
    
    print("CKR")
    lm =CKR.getLm(weights, monitors)
    #print("Lm:{}".format(lm))
    res = getMinTra(edgesLabel, lm, paths, t, tmax, x0)        
    #print("result:{}".format(res))
    pos=plg.plot(g, weights, monitors, lm, pos)
    allres.append(res[0])
    alllm.append(len(lm))
    percList = [1, 5, 10, 15, 20]
    for perc in percList:
        print("{}% top traversal".format(perc))
        lm = topTraversal(perc, weights)
        #print("Lm:{}".format(lm))
        res = getMinTra(edgesLabel, lm, paths, t, tmax, x0)
        #print("result:{}".format(res))
        plg.plot(g, weights, monitors, lm, pos)
        allres.append(res[0])
        alllm.append(len(lm))
    print(allres)
    print(alllm)
    #pathc = pathThrCount(paths)
    #print ("paths:")
    #showPathsByEdge(paths, edgesLabel)
    
    #allHit, minall, nonAllHit, maxnonall = getAllHitRes(paths, labelEdge, results)
    
            
    