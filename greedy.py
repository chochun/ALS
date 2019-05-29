import pygraphml

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

def greedy(weights, paths):
    #initialize paths and links
    beCutPaths=paths.copy()
    Lm = []
    while beCutPaths:        
        #set the initial value for greedy
        minCost = float("inf")
        l = 0
        #update pl 
        pl = getPl(beCutPaths)
        for e, _ in pl.items():
            cost = (weights[e]/len(pl[e]))
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
        #print("beCutPaths:{}".format(len(beCutPaths)))
        #print("paths:{}".format(len(paths)))
        progress = 1-(len(beCutPaths)/(len(paths)))
        print("progress:{}".format(progress))
    return Lm