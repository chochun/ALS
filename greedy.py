import pygraphml
import pathHandler

def greedy(weights, paths, budget, isCALS):
    #initialize paths and links
    beCutPaths=paths.copy()
    Lm = []
    edges = pathHandler.getEdges(weights)
    while beCutPaths:
        if len(Lm) == budget:
            break
        #update pl
        pl = pathHandler.getPl(beCutPaths)
        l = 0
        
        #CALS
        if isCALS:
            maxdiffTm = float("-inf")
            currentTm = pathHandler.getTm(edges, Lm, paths)
            for e, _ in pl.items():
                diffTm = pathHandler.getTm(edges, Lm + [e], paths) - currentTm
                if diffTm > maxdiffTm:
                    maxdiffTm = diffTm
                    l=e
                    
        #ALS
        else:
            #set the initial value for greedy
            minCost = float("inf")
            for e, _ in pl.items():
                cost = (weights[e]/len(pl[e]))
                if cost < minCost:
                    minCost = cost
                    l = e
               
        #update Lm by the smallest cost
        Lm.append(l)
        
        for path in pl[l]:
            #update the paths being cut
            beCutPaths.remove(path)
            
        #printing process
        progress = (1-(len(beCutPaths)/(len(paths))))*100
        print("progress:{}".format(progress))
    return Lm