from pygraphml import Graph
from pygraphml import GraphMLParser
import numpy as np
import optimizer as opt
import itertools

def getAdjNodes(node):
    nodes = []
    for e in node.edges():
        if e.node1 != node:
            nodes.append(e.node1)
        if e.node2 != node:
            nodes.append(e.node2)
    return nodes

def DFS(u, t, visited, path, paths):
    visited[u["label"]] = True
    path.append(u)
    if u == t:
        paths.append(path[:])
    else:
        for n in getAdjNodes(u):
            if not visited[n["label"]]:
                DFS(n, t, visited, path, paths)
    path.pop()
    visited[u["label"]] = False    

def getAllPathsByNode(s, t, g):
    paths = []
    path = []
    visited = {}
    for n in g.nodes():
        visited[n["label"]] = False
    DFS(s, t, visited, path, paths)
    return paths

def pathThrCount(paths):
    count = {}
    for p in paths:
        for e in p:
            count[e] = count.get(e, 0) + 1
    return count
    
def getAllPathsByEdge(s, t, g):
    pathsN = []
    pathsE = []
    path = []
    visited = {}
    for n in g.nodes():
        visited[n["label"]] = False
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
    return pathsE

def placeMonitors(g):        
    monitors = []
    for n in g.nodes():
        #if n["label"]=="0" or n["label"]=="1" or n["label"]=="2" or n["label"]=="6" or n["label"]=="7":
        if len(n.edges()) == 1:
        #if n["label"]=="0" or n["label"]=="5" or n["label"]=="10":    
            monitors.append(n)
    return monitors

def showPathsByNode(paths):
    for path in paths:
        pstring = "-"
        for n in path:
            pstring = pstring + n["label"] + "-"
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


if __name__ == "__main__":
    parser = GraphMLParser()
    #bridge3, star5,
    #g = parser.parse("./archive/house3.graphml")
    g = parser.parse("./archive/bridge2.graphml")
    g.show(show_label=True)
    #get R
    #monitors
    monitors = placeMonitors(g)
    
    #establish label for edges
    edgesLabel = {}
    i = 0
    for e in g.edges():
        edgesLabel[e] = i
        i+=1
    
    labelEdge = {}
    for edge, l in edgesLabel.items():
        labelEdge[l] = edge
    #nLinks = len(edgesLabel)
    allpaths = []
    #pp = []
    for i in range(len(monitors)):
        for j in range(i+1, len(monitors)):
            allpaths += getAllPathsByEdge(monitors[i], monitors[j], g)
            #pp += getAllPathsByNode(monitors[i], monitors[j], g)
    
    paths = allpaths  
    """
    somepaths = []
    somepaths.append(allpaths[0])
    somepaths.append(allpaths[1])
    somepaths.append(allpaths[2])
    somepaths.append(allpaths[3])
    somepaths.append(allpaths[4])
    paths = somepaths        
    """
    maxd = (0,[])
    t = 5
    tmax = 11
    x0 = np.zeros(len(edgesLabel))
    for i in range(x0.size):
        x0[i] = t
    results = []
    ### create lm
    for n in range(1, len(edgesLabel)+1):
        for lm in itertools.combinations(range(len(edgesLabel)), n):
            print(lm)
            ### create pm, pn from lm
            pm = []
            pn = []
            
            
            #if 3 in lm:
            #    continue
            for path in paths:
                isNormal = True
                for e in path:
                    if edgesLabel[e] in lm:
                        isNormal = False
                        pm.append(path)
                        break
                if isNormal:
                    pn.append(path)
            print ("pn:")
            showPathsByEdge(pn, edgesLabel)        
            print ("pm:")
            showPathsByEdge(pm, edgesLabel)  
            
            ### create rm, rn from pm, pn
            rm = getArr(pm, edgesLabel)
            rn = getArr(pn, edgesLabel)
            print("rn:")
            print(rn)
            print("rm:")
            print(rm)            
            res = opt.maxdam(rn, rm, lm, t, tmax, x0)
            print("res:{}".format(res))
            results.append(res)
            if res[0] > maxd[0]:
                maxd = res
    pathc = pathThrCount(paths)
    print ("paths:")
    showPathsByEdge(paths, edgesLabel)
    
    allHit, minall, nonAllHit, maxnonall = getAllHitRes(paths, labelEdge, results)
    if minall >= maxnonall:
        print ("minall >= maxnonall")
    else:
        print ("minall <= maxnonall")
    #print("")
    #showPathsByNode(pp)
    
            
    