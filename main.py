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
import dijkstra as dij
import importMatlab as ipM
import pathHandler as paH

def getArr(paths, edgesLabel):
    nLinks = len(edgesLabel)
    arr = np.zeros((len(paths), nLinks))
    for i in range(len(paths)):
        for e in paths[i]:
            j = edgesLabel[e]
            arr[i,j] = 1
    return arr

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


if __name__ == "__main__":
    expinfo={}
    #set up initial value:t, tmax
    init = 10
    t = 150
    tmax = 2000
    numberMonitor = 4
    numberMonitors = [numberMonitor] #[4,5,6,7,8]#[20,21,22,23,24,25]#[10,11,12,13,14,15]#[4,5,6,7,8]#[10,11,12,13,14,15]
    loops = 1 #how many times for each number of monitors
    
    #monitors, paths
    cond = "one" #one=> place monitors at 1-degree nodes; any=> place monitors at any nodes 
    degreeLimit = 1
    #numberPathsBtw2M = float('inf')
    
    #SP: shortest path, All: all possible path
    routing = "All"
    
    
    #"$\infty$" is used for plotting infinity symbol
    #budget = -1: every algorithm will run until getting a cut
    #budget = -2: CKR and greedy will run until getting a cut, top traversal and random will run until |Lm|== |Lm| of CKR
    #budget = k: every algorithm will stop when either |Lm|==k or getting a cut
    budget = -1
    budgets = [budget]#[21,22,23,24,25,-1]#[9,10,11,12,13,-1]#[2,3,4,5,6,-1]
    
    #methods = ["greedy", "CKR", "top traversal", "random", "all"]
    #methods = ["CALS greedy", "ALS greedy", "top traversal", "random"]
    #methods = ["top traversal", "random"]
    methods = ["all", "CKR"]
    #methods = ["CKR", "top traversal", "random"]
    allres = []
    allginfo = []
    CALSlm = []
    ALSlm = []
    allpms = []
    alllms = []
    #alllsPn = []
    #lllsPm = []
    #allpmlengths = []
    #allpmdiverse = []
    #alllsPnOnPm = []
    #alltermWithoutConst = []
    ginfos = ["nodes", "paths", "edges"]
    #alllinks = []
    #get the graph
    
    parser = GraphMLParser()
    gname= "bridge2"#"Bics"#"BeyondTheNetwork"#"Cogentco"#"bridge2"#"BeyondTheNetwork"#"Getnet"
    g = parser.parse("./archive/{}.graphml".format(gname))
    """
    #pmlengths = ["top 1 traversal", "avg"]
    gname="AS20965"#"AS8717"#"AS20965"#"AS8717"
    g = ipM.loadgraph("./MatlabData/CAIDA_{}.mat".format(gname))
    """
    expinfo["init"]=init
    expinfo["t"]=t
    expinfo["tmax"]=tmax
    expinfo["numberMonitors"]=numberMonitors
    expinfo["loops"]=loops
    expinfo["cond"]=cond
    #expinfo["numberPathsBtw2M"]=numberPathsBtw2M
    expinfo["gname"]=gname
    expinfo["budgets"] = budgets
    expinfo["# of nodes with {} degree".format(degreeLimit)]= paH.getnNodes(g, degreeLimit)
    print(expinfo)
    #monitors, and then get paths
    #numberMonitor = 3
    #numberPathsBtw2M = 5
    #monitors = paH.placeMonitors(g, numberMonitor)
    #for budget in budgets:
    for numberMonitor in numberMonitors:
        res = {me:[] for me in methods}
        #npms = {me:[] for me in methods}
        #nlsPn = {me:[] for me in methods}
        #nlsPm = {me:[] for me in methods}
        #termNoConst = {me:[] for me in methods}
        #nlsPnOnPm = {me:[] for me in methods}
        #pmdiverse = {me:[] for me in methods}
        graphinfo = {ginfo:[] for ginfo in ginfos}
        numberLm = {me:[] for me in methods}
        numberPm = {me:[] for me in methods}
        #pmlength = {p:[] for p in pmlengths}
        #links = {me:[] for me in methods}
        
        for l in range(loops):
            monitors = paH.placeMonitors(g, numberMonitor, cond)
            paths = []
            for i in range(len(monitors)):
                for j in range(i+1, len(monitors)):
                    if routing == "All":
                        paths += paH.getPathsByEdge(monitors[i], monitors[j], g, float('inf'))
                    elif routing == "SP":
                        paths += dij.shortestpath(g, 1.0, monitors[i], monitors[j])
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
            
            weights = paH.getWeight(paths)
            nodes = paH.getNodes(weights)
            edges = paH.getEdges(weights)
            print("# of nodes:{}".format(len(nodes)))
            graphinfo["nodes"].append(len(nodes))
            print("# of edges:{}".format(len(edges)))
            graphinfo["edges"].append(len(edges))
            
            ### length of Pm
            """
            top1AvgLen = paH.countAvgLength(paH.getPm(paths, [paH.getMostTraversal(weights)]))
            pmlength["top 1 traversal"].append(top1AvgLen)
            print("top1AvgLen:{}".format(top1AvgLen))
            avgLen = paH.countAvgLength(paths)
            pmlength["avg"].append(avgLen)
            print("avgLen:{}".format(avgLen))
            """
            LMs = []
            for method in methods:
                print(method)
                if method=="ALS greedy" or method=="greedy":
                    lm = gd.greedy(weights, paths, budget, isCALS=False)
                    if budget == -1:
                        ALSlm.append(len(lm))
                    #pos=plg.plot(g, weights, monitors, lm)
                elif method=="CALS greedy":
                    lm = gd.greedy(weights, paths, budget, isCALS=True)
                    if budget == -1:
                        CALSlm.append(len(lm))
                elif method=="CKR":
                    lm = CKR.getLm(weights, monitors)
                    CKRlm = len(lm)
                    #pos=plg.plot(g, weights, monitors, lm)
                elif method=="random":
                    if budget == -1:
                        lm = paH.randomLmCut(edges, paths)
                    elif budget == -2:
                        lm = paH.randomLm(edges, CKRlm)
                    else:
                        nlm = budget
                        lm = paH.randomLm(edges, nlm)
                elif method=="top traversal":
                    if budget == -1:
                        lm = paH.topTraversalCut(weights, paths)
                    elif budget == -2:
                        lm = paH.topTraversal(CKRlm, weights)
                    else:
                        nlm = budget
                        lm = paH.topTraversal(nlm, weights)
                    #pm diverse
                elif method=="all":
                    lm = edges
                LMs.append(lm)               
                print("# of lm:{}".format(len(lm)))
                numberLm[method].append(len(lm))
                numberPm[method].append(paH.countPm(lm, paths))
                #npms[method].append(paH.countPm(lm, paths))
                #nlsPn[method].append(paH.countNLinksofPn(lm, paths))
                #nlsPm[method].append(paH.countNLinksofPm(lm, paths))
                #nlsPnOnPm[method].append(paH.countNLinksofPnOnPm(lm, paths))
                #pmdiverse[method].append(paH.getTotalTraversalNumber(paths,lm))
                #termNoConst[method].append(paH.getTermWithoutCons(edges, lm, paths))
                #numberOfLinks = paH.countNLinksofPn(lm, paths) + paH.countNLinksofPm(lm, paths) - paH.countNLinksofPnOnPm(lm, paths)
                #links[method].append(numberOfLinks)
                objv = getMinTra(edgesLabel, lm, paths, t, tmax, x0)        
                #pos=plg.plot(g, weights, monitors, lm, pos)
                res[method].append(objv[0])
        #print(LMs)
        plg.plot(g, weights, monitors, LMs)    
        allres.append(res)
        alllms.append(numberLm)
        allpms.append(numberPm)
        #allpms.append(npms)
        #alllsPn.append(nlsPn)
        #alllsPm.append(nlsPm)
        #alllsPnOnPm.append(nlsPnOnPm)
        allginfo.append(graphinfo)
        #alltermWithoutConst.append(termNoConst)
        #allpmlengths.append(pmlength)
        #allpmdiverse.append(pmdiverse)
        #alllinks.append(links)
    
    #plb.plot(allres, methods, budgets, gname, None, multiple=False)
    #plb.plot(allginfo, ginfos, numberMonitors, gname, multiple=False)
    #plb.plot(allpms, ginfos, numberMonitors, gname)
    expinfo["ALSlm"] = ALSlm
    expinfo["CALSlm"] = CALSlm
    #paH.showAvgStd(allginfo)
    """
    res_out = open("./experiment-CALS/infinite budget/{}/res.pickle".format(gname),"wb")
    pickle.dump(allres, res_out)
    res_out.close()
    
    res_out = open("./experiment-CALS/infinite budget/{}/lms.pickle".format(gname),"wb")
    pickle.dump(alllms, res_out)
    res_out.close()
    
    res_out = open("./experiment-CALS/infinite budget/{}/pms.pickle".format(gname),"wb")
    pickle.dump(allpms, res_out)
    res_out.close()
    
    graph_out = open("./experiment-CALS/infinite budget/{}/graph.pickle".format(gname),"wb")
    pickle.dump(allginfo, graph_out)
    graph_out.close()
    
    expinfo_out = open("./experiment-CALS/infinite budget/{}/expinfo.pickle".format(gname),"wb")
    pickle.dump(expinfo, expinfo_out)
    expinfo_out.close()
    """
    
    
            
    
    