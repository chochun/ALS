from pygraphml import Graph
from pygraphml import GraphMLParser
import numpy as np
import optimizer as opt
import itertools
import greedy as gd
import operator
import plottopology as plg
import plotbargraph as plb
import CKR
import pickle

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

def placeMonitors(g, amount, con):        
    monitors = []
    nodes = []
    if con=="any":
        nodes = g.nodes()
    elif con=="one":
        for n in g.nodes():
            if len(n.edges())==1:
                nodes.append(n)
    elif con=="two":
        nodes1 = []
        for n in g.nodes():
            if len(n.edges())==1:
                nodes1.append(n)
        if len(nodes1) < amount:
            monitors = nodes1[:]
            amount = amount - len(nodes1)
            for n in g.nodes():
                if len(n.edges())==2:
                    nodes.append(n)
        else:
            nodes = nodes1[:]
    elif con=="onetwo":
        for n in g.nodes():
            if len(n.edges())<=2:
                nodes.append(n)
    
    selectedNodes = np.random.choice(len(nodes), amount, replace=False)
    print("selectedNodes:{}".format(selectedNodes))
    for i in selectedNodes:
        #put the monitors to the points which are connected by a single link.
        #if len(n.edges()) == 1:
        monitors.append(nodes[i])
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

def topTraversal(number, weight):
    lm = []
    #number = int(np.ceil((percentile/100)*len(weight)))
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

def randomLm(edges, amount):
    lm = []
    selected = np.random.choice(len(weights), amount, replace=False)
    for i in selected:
        lm.append(edges[i])
    return lm
        
if __name__ == "__main__":
    expinfo={}
    #set up initial value:t, tmax
    init = 10
    t = 150
    tmax = 2000
    numberMonitors = [4,5,6,7,8]
    loops = 20 #how many times for each number of monitors
    
    #monitors, paths
    cond = "onetwo" #one=> place monitors at 1-degree nodes; any=> place monitors at any nodes 
    numberPathsBtw2M = float('inf')
    
    methods = ["greedy", "CKR", "top traversal", "random", "all"]
    allres = []
    allginfo = []
    #get the graph
    parser = GraphMLParser()
    gname="Bics"
    g = parser.parse("./archive/{}.graphml".format(gname))
    
    expinfo["init"]=init
    expinfo["t"]=t
    expinfo["tmax"]=tmax
    expinfo["numberMonitors"]=numberMonitors
    expinfo["loops"]=loops
    expinfo["cond"]=cond
    expinfo["numberPathsBtw2M"]=numberPathsBtw2M
    expinfo["gname"]=gname
    
    #monitors, and then get paths
    #numberMonitor = 3
    #numberPathsBtw2M = 5
    #monitors = placeMonitors(g, numberMonitor)
    for numberMonitor in numberMonitors:
        res = {}
        for me in methods:
            res[me]=[]
        graphinfo={}
        ginfos = ["nodes", "paths", "edges"]
        for ginfo in ginfos:
            graphinfo[ginfo]=[]
        for l in range(loops):
            monitors = placeMonitors(g, numberMonitor, cond)
            allpaths = []
            for i in range(len(monitors)):
                for j in range(i+1, len(monitors)):
                    allpaths += getPathsByEdge(monitors[i], monitors[j], g, numberPathsBtw2M)
            paths = allpaths
            print("paths are defined")
            print("# of paths:{}".format(len(paths)))
            graphinfo["paths"].append(len(paths))
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
            for i in range(x0.size):
                x0[i] = init
            
            weights = getWeight(paths)
            nodes = getNodes(weights)
            edges = getEdges(weights)
            print("# of nodes:{}".format(len(nodes)))
            graphinfo["nodes"].append(len(nodes))
            print("# of edges:{}".format(len(edges)))
            graphinfo["edges"].append(len(edges))    
            
            numberCKRLm = -1
            for method in methods:
                print(method)
                if method=="greedy":
                    lm = gd.greedy(weights, paths)
                elif method=="CKR":
                    lm = CKR.getLm(weights, monitors)
                    numberCKRLm = len(lm)
                elif method=="random":
                    lm = randomLm(edges, numberCKRLm)
                elif method=="top traversal":
                    lm = topTraversal(numberCKRLm, weights)
                elif method=="all":
                    lm = edges
                print("# of lm:{}".format(len(lm)))
                objv = getMinTra(edgesLabel, lm, paths, t, tmax, x0)        
                #pos=plg.plot(g, weights, monitors, lm)
                res[method].append(objv[0])    
        allres.append(res)
        allginfo.append(graphinfo)
    plb.plot(allres, methods, numberMonitors, gname)
    plb.plot(allginfo, ginfos, numberMonitors, gname)
    
    res_out = open("res.pickle","wb")
    pickle.dump(allres, res_out)
    res_out.close()
    
    graph_out = open("graph.pickle","wb")
    pickle.dump(allginfo, graph_out)
    graph_out.close()
    
    expinfo_out = open("expinfo.pickle","wb")
    pickle.dump(expinfo, expinfo_out)
    expinfo_out.close()
    
    
    
    
            
    