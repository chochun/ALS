from gurobipy import *
import numpy

def maxdam(rn, rm, lm, t, tmax, x0):
    npn = rn.shape[0]
    npm = rm.shape[0]
    nlinks = rm.shape[1]
    pi = [t if (i in lm) else tmax for i in range(nlinks)]
    #print(pi)
    m = Model("optimization")
    xe = m.addVars(nlinks, vtype=GRB.CONTINUOUS)
    #x = [1]*nlinks
    m.setObjective(quicksum(quicksum(rm[i,j]*xe[j] for j in range(nlinks))- rm.dot(x0)[i] for i in range(npm)), GRB.MAXIMIZE)
    #print([sum(rm[i,j]*x[j] for j in range(nlinks))- rm.dot(x0)[i] for i in range(npm)])
    m.addConstrs(quicksum(rn[i,j]*xe[j] for j in range(nlinks)) == rn.dot(x0)[i]  for i in range(npn))
    #print([sum(rn[i,j]*x[j] for j in range(nlinks)) == rn.dot(x0)[i]  for i in range(npn)])
    m.addConstrs(xe[i] <= pi[i] for i in range(nlinks))
    m.optimize()
    if m.status != 2:
        print("Model not OPTIMAL - status: ", m.status)
        raise
    xee = x0.copy()
    
    for i in range(nlinks):
        xee[i] = xe[i].x
    objv = numpy.sum(rm.dot(xee-x0))
    return (objv, m.ObjVal, lm, xee)