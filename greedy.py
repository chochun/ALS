import pygraphml

# Pl is a set of paths traversing the link l
def getPl(paths, edges):
    pl = {}
    for e in edges:
        pl[e] = []
    for path in paths:
        for e in path:
            if path not in pl[e]:
                pl[e].append(path)
    return pl

def greedy(graph, weight, paths):
    #initialize paths and links
    beCutPaths=paths.copy()
    Lm = []
    while beCutPaths:        
        #set the initial value for greedy
        minCost = float("inf")
        l=0
        #update cost for each edge. 
        #wminus = getWeight(beCutPaths)
        pl = getPl(beCutPaths, graph.edges())
        for e in graph.edges():
            #ensure the link is traversed by at least 1 path
            if len(pl[e]) != 0: 
                cost = (weight[e]/len(pl[e]))
                if cost < minCost:
                    minCost = cost
                    l = e
        #update Lm by the smallest cost
        if type(l) != pygraphml.edge.Edge:
            print("the link with the smallest cost failed to be selected")
            raise
        Lm.append(l)
        
        for path in pl[l]:
            #update the paths being cut
            beCutPaths.remove(path)
            
        #printing process
        progress = 1-(len(beCutPaths)/(len(paths)))
        print("progress:{}".format(progress))
    return Lm