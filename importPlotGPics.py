

import pickle
import plotbargraph as plb

#ALS
allres = [[pickle.load(open("./experiment2/case2/res.pickle", "rb")), pickle.load(open("./experiment2/case1/res.pickle", "rb"))], 
           [pickle.load(open("./experiment2/case5/res.pickle", "rb")), pickle.load(open("./experiment2/case3/res.pickle", "rb"))], 
           [pickle.load(open("./experiment2/case7/res.pickle", "rb")), pickle.load(open("./experiment2/case8/res.pickle", "rb"))]]
numberMonitors = [[[4,5,6,7,8], [4,5,6,7,8]], [[10,11,12,13,14,15], [10,11,12,13,14,15]], [[20,21,22,23,24,25], [20,21,22,23,24,25]]]
methods = ["greedy", "CKR", "top traversal", "random", "all"]
allginfo = [[pickle.load(open("./experiment2/case2/graph.pickle", "rb")), pickle.load(open("./experiment2/case1/graph.pickle", "rb"))], 
           [pickle.load(open("./experiment2/case5/graph.pickle", "rb")), pickle.load(open("./experiment2/case3/graph.pickle", "rb"))], 
           [pickle.load(open("./experiment2/case7/graph.pickle", "rb")), pickle.load(open("./experiment2/case8/graph.pickle", "rb"))]]
gname = [["Bics", "BTN"], ["Colt", "Cogent"], ["AS 20965", "AS 8717"]]
#plb.plot(allres, methods, numberMonitors, gname, None, multiple=True)
plb.plot(allres, methods, numberMonitors, gname, allginfo, multiple=True)
"""
#CALS
allres = [[pickle.load(open("./experiment-CALS/case 4/res.pickle", "rb")), pickle.load(open("./experiment-CALS/case 3/res.pickle", "rb"))], 
           [pickle.load(open("./experiment-CALS/case 2/res.pickle", "rb")), pickle.load(open("./experiment-CALS/case 1/res.pickle", "rb"))], 
           [pickle.load(open("./experiment-CALS/case 5/res.pickle", "rb")), pickle.load(open("./experiment-CALS/case 6/res.pickle", "rb"))]]

for i in range(len(allres)):
    for j in range(len(allres[i])):
        for k in range(len(allres[i][j])):
            allres[i][j][k]["greedy ALS"] = allres[i][j][k]["ALS greedy"]
            allres[i][j][k]["greedy CALS"] = allres[i][j][k]["CALS greedy"]

numberMonitors = [[[2, 3, 4, 5, 6, "$\infty$"], [2, 3, 4, 5, 6, "$\infty$"]], [[9, 10, 11, 12, 13, "$\infty$"], [9, 10, 11, 12, 13, "$\infty$"]], [[21,22,23,24,25,"$\infty$"], [21,22,23,24,25,"$\infty$"]]]
methods = ["greedy ALS", "greedy CALS", "top traversal", "random"]
allginfo = [[pickle.load(open("./experiment-CALS/case 4/graph.pickle", "rb")), pickle.load(open("./experiment-CALS/case 3/graph.pickle", "rb"))], 
           [pickle.load(open("./experiment-CALS/case 2/graph.pickle", "rb")), pickle.load(open("./experiment-CALS/case 1/graph.pickle", "rb"))], 
           [pickle.load(open("./experiment-CALS/case 5/graph.pickle", "rb")), pickle.load(open("./experiment-CALS/case 6/graph.pickle", "rb"))]]
gname = [["Bics", "BTN"], ["Colt", "Cogent"], ["AS 20965", "AS 8717"]]
#plb.plot(allres, methods, numberMonitors, gname, None, multiple=True)
plb.plot(allres, methods, numberMonitors, gname, allginfo, multiple=True)
"""