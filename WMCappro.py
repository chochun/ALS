# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 16:24:08 2019

@author: cuc496
"""
"""
L: limit of the sum of cost
X=[e1, e2, ..., en]
weights={e1 => w1, e2 => w2, ...}
S=[s1, s2, ..., sm]
sets={s1=>[e1,e2], s2=>[], }
costs={s1 => c1, s2 => c2, ...}
H = a subset of S
U = a subset of S
"""
def getcost(H, costs):
    res = 0
    for s in H:
        res += costs[s]
    return res

def getweightfromsNotInH(H, s, weights, sets):
    res = 0
    eH = {}
    for i in range(len(H)):
        for e in sets[H[i]]:
            eH[e] = True
    for ele in sets[s]:
        if ele not in eH:
            res += weights[ele]
    return res

def greedy(H, U, weights, costs, sets, L):
    while len(U)>0:
        #greedy: select the best set
        a = float("-inf")
        selecteds = 0
        for s in U:
            sa = getweightfromsNotInH(H, s, weights, sets)/costs[s]
            if sa>=a:
                a = sa
                selecteds = s
        if getcost(H,costs)+costs[selecteds]<=L:
            H.append(selecteds)
        U.remove(selecteds)
    return H

def getweightfromH(H, weights, sets):
    res = 0
    eDic = {}
    for s in H:
        for e in sets[s]:
            eDic[e] = True
    #print(eDic)
    for e in eDic:
        res += weights[e]
    return res

def getWMCSet(S, X, weights, sets, costs, L):
    wH1 = float("-inf")
    H1 = []
    
    #|subsets|==1
    for s in S:
        H = [s]
        if getcost(H, costs)<=L:
            w = getweightfromH(H, weights, sets)
            if wH1<=w:
                wH1=w
                H1=H
    
    #|subsets|==2
    for i in range(len(S)):
        for j in range(i+1, len(S)):
            H = [S[i], S[j]]
            if getcost(H, costs)<=L:
                w = getweightfromH(H, weights, sets)
                if wH1<=w:
                    wH1=w
                    H1=H
    
    wH2 = float("-inf")
    H2 = []
    
    #|subsets|==3
    for i in range(len(S)):
        for j in range(i+1, len(S)):
            for k in range(j+1, len(S)):
                H = [S[i], S[j], S[k]]
                if getcost(H, costs)<=L:
                    U = S[:]
                    U.remove(S[i])
                    U.remove(S[j])
                    U.remove(S[k])
                    H = greedy(H, U, weights, costs, sets, L)
                    w = getweightfromH(H, weights, sets)
                    if wH2<=w:
                        wH2=w
                        H2=H
    print(wH1)
    print(H1)
    print(wH2)
    print(H2)
    if wH1>wH2:
        return H1
    else:
        return H2
    
    