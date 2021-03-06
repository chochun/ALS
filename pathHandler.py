import numpy as np
import operator

#when lm only contains a single link, it returns the traversed paths
def getPm(paths, lm):
    pm = []
    for path in paths:
        isPm = False
        for e in path:
            if e in lm:
                isPm = True
                break
        if isPm:
            pm.append(path)
    return pm

def countPm(lm, paths):
    n = 0
    for path in paths:
        for e in path:
            if e in lm:
                n += 1
                break
    return n

def isCut(lm, paths):
    return countPm(lm, paths)==len(paths)

def getnNodes(g,degree):
    k = 0
    for n in g.nodes():
        if len(n.edges())<=degree:
            k+=1
    return k

def getNodes(weights):
    nodes = []
    for e, w in weights.items():
        if e.node1 not in nodes:
            nodes.append(e.node1)
        if e.node2 not in nodes:
            nodes.append(e.node2)
    return nodes

def getPn(paths, lm):
    Pn = []
    Pm = getPm(paths, lm)
    for path in paths:
        if path not in Pm:
            Pn.append(path)
    return Pn

# Pl is a set of paths traversing the link l
def getPl(paths):
    pl = {}
    for path in paths:
        for e in path:
            if e not in pl:
                pl[e] = []
            if path not in pl[e]:
                pl[e].append(path)
    return pl

def getWeight(paths):
    weights={}
    for path in paths:
        for e in path:
            weights[e] = weights.get(e, 0) + 1
    return weights

def isEdgeinPm(edge, Pm):
    for path in Pm:
        if edge in path:
            return True
    return False

def isEdgeinPn(edge, Pn):
    for path in Pn:
        if edge in path:
            return True
    return False

def getEdgeWithoutConst(edges, lm, Pm, Pn):
    noConstEdges = []
    for e in edges:
        if isEdgeinPm(e, Pm) and (e not in lm) and (not isEdgeinPn(e, Pn)) and (e not in noConstEdges):
            noConstEdges.append(e)
    return noConstEdges

def getEdges(weights):
    edges = []
    for e, w in weights.items():
        if e not in edges:
            edges.append(e)
    return edges

def getEdgesFromP(paths):
    edges = []
    for path in paths:
        for e in path:
            if e not in edges:
                edges.append(e)
    return edges

def getTm(edges, lm, paths):
    Tm = 0
    if not lm:
        return Tm
    Pm = getPm(paths, lm)
    Pn = getPn(paths, lm)
    noConstEdges = getEdgeWithoutConst(edges, lm, Pm, Pn)
    traversalofPm = getWeight(Pm)
    for e in noConstEdges:
        Tm += traversalofPm[e]
    return Tm


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


def pathThrCount(paths):
    count = {}
    for p in paths:
        for e in p:
            count[e] = count.get(e, 0) + 1
    return count

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
    #selectedNodes = [0,5]
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

def topTraversal(number, weights, costs):
    lm = []
    budgetcost = 0
    sortedLinkByTraveral = sorted(weights.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(len(weights)):
        if (budgetcost + costs[sortedLinkByTraveral[i][0]]) <= number:
            lm.append(sortedLinkByTraveral[i][0])
            budgetcost += costs[sortedLinkByTraveral[i][0]]
    return lm

def topTraversalCut(weight, paths):
    lm = []
    sortedLinkByTraveral = sorted(weight.items(), key=operator.itemgetter(1), reverse=True)
    i=0
    while not isCut(lm, paths):
        i += 1        
        lm.append(sortedLinkByTraveral[i][0])
    return lm

def randomLm(edges, amount, costs):
    lm = []
    budgetcost = 0
    selected = np.random.choice(len(edges), amount, replace=False)
    for i in selected:
        if (budgetcost + costs[edges[i]]) <= amount:
            lm.append(edges[i])
            budgetcost += costs[edges[i]]
    return lm

def randomLmCut(edges, paths):
    lm = []
    amount = 0
    while not isCut(lm, paths):
        amount += 1
        selected = np.random.choice(len(edges), amount, replace=False)
        for i in selected:
            lm.append(edges[i])
    return lm

def countNLinksofPnOnPm(lm, paths):
    linksOfPm = {}
    linksOfPnOnPm = {}
    pm = getPm(paths, lm)
    for path in pm:
        for e in path:
            linksOfPm[e] = 1
    for path in paths:
        if path not in pm:
            for e in path:
                if e in linksOfPm:
                    linksOfPnOnPm[e]= 1
    return len(linksOfPnOnPm)

def countNLinksofPn(lm, paths):
    linksOfP = {}
    for path in paths:
        isPm = False
        for e in path:
            if e in lm:
                isPm = True
                break
        if not isPm:
            for e in path:
                linksOfP[e]= 1
    return len(linksOfP)

def countNLinksofPm(lm, paths):
    linksOfP = {}
    for path in paths:
        isPm = False
        for e in path:
            if e in lm:
                isPm = True
                break
        if isPm:
            for e in path:
                linksOfP[e]= 1
    return len(linksOfP)

def getMostTraversal(weights):
    return sorted(weights.items(),key=operator.itemgetter(1), reverse=True)[0][0]

def showAvgStd(allginfo):
    nodes = []
    edges = []
    paths = []
    for group in allginfo:
        for k, v in group.items():
            stat = "{}({})".format(np.average(v), np.std(v))
            if k == "nodes":
                nodes.append(stat)
            elif k == "edges":
                edges.append(stat)
            elif k == "paths":
                paths.append(stat)
    print(nodes)
    print(edges)
    print(paths)

def getTraversalNumber(paths, link):
    return len(getPm(paths, [link]))

def getAvgLmPerPath(paths, lm):
    overlap = 0
    for e in lm:
        overlap += getTraversalNumber(paths, e)
    numberPm = len(getPm(paths, lm))
    return overlap/numberPm

def getTotalTraversalNumber(paths, lm):
    overlap = 0
    for e in lm:
        overlap += getTraversalNumber(paths, e)
    return overlap

def getTermWithoutCons(edges, lm, paths):
    Pm = getPm(paths, lm)
    Pn = getPn(paths, lm)
    noConstEdges = getEdgeWithoutConst(edges, lm, Pm, Pn)
    termsSum = 0
    traversalofPm = getWeight(Pm)
    for e in noConstEdges:
        termsSum += traversalofPm[e]
    return termsSum

def countAvgLength(paths):
    lengths = []
    print("len of paths:{}".format(len(paths)))
    for path in paths:
        lengths.append(len(path))
    return np.average(lengths)
