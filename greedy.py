import pygraphml
import pathHandler

def greedy(weights, costs, paths, budget, isCALS):
    #initialize paths and links
    beCutPaths=paths.copy()
    Lm = []
    budgetcost = 0
    edges = pathHandler.getEdges(weights)
    while beCutPaths:
        #update pl
        pl = pathHandler.getPl(beCutPaths)
        l = 0
        
        #CALS
        if isCALS:
            maxdiffTm = float("-inf")
            currentTm = pathHandler.getTm(edges, Lm, paths)
            for e, _ in pl.items():
                if (budgetcost+costs[e])<=budget:
                    diffTm = pathHandler.getTm(edges, Lm + [e], paths) - currentTm
                    if diffTm > maxdiffTm:
                        maxdiffTm = diffTm
                        l=e
            #a termination condition: when no link can be compromised
            if maxdiffTm == float("-inf"): 
                break
                    
        #ALS
        else:
            #set the initial value for greedy
            minC = float("inf")
            for e, _ in pl.items():
                if (budgetcost+costs[e])<=budget:
                    c = (weights[e]/len(pl[e]))
                    if c < minC:
                        minC = c
                        l = e
                        
            #a termination condition: when no link can be compromised
            if minC == float("inf"): 
                break
               
        #update Lm by the best selection
        Lm.append(l)
        budgetcost += costs[l]
        
        for path in pl[l]:
            #update the paths being cut
            beCutPaths.remove(path)
            
        #printing process
        progress = (1-(len(beCutPaths)/(len(paths))))*100
        print("progress:{}".format(progress))
    return Lm