import matplotlib
import matplotlib.pyplot as plt
import numpy as np
def autolabel(ax, rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')

def plot(allres, xgroups, xlabels, gname):
    means = {}
    stds = {}
    for method in xgroups:
        means[method] = []
        stds[method] = []
    
    for r in allres:
        for method in xgroups:
            means[method].append(np.average(r[method]))
            stds[method].append(np.std(r[method]))
    
    ylabel = "Objective value"
    title = gname
    #men_means, men_std = (20, 35, 30, 35, 27), (2, 3, 4, 1, 2)
    #women_means, women_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)
    
    ind = np.arange(len(xlabels))  # the x locations for the groups
    width = 0.6  # the width of the bars
    
    fig, ax = plt.subplots()
    
    
    #rects1 = ax.bar(ind - width/2, men_means, width, yerr=men_std,
    #                label='Men')
    #rects2 = ax.bar(ind + width/2, women_means, width, yerr=women_std,
    #                label='Women')
    
    w = [ind-width/2+width/(2*len(xgroups))]
    for i in range(len(xgroups)-1):
        ww = w[i]+width/len(xgroups)
        w.append(ww)
    # Add some text for labels, title and custom x-axis tick labels, etc.
    
    
    #autolabel(rects1, "left")
    #autolabel(rects2, "right")
    
    
    #w = [ind - width/2, ind + width/2]
    for i in range(len(xgroups)):
        ax.bar(w[i], means[xgroups[i]], width/len(xgroups), 
                       yerr=stds[xgroups[i]], label=xgroups[i])
        #autolabel(ax, rects, "center")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(xlabels)
    ax.legend(loc='best')
    fig.tight_layout()
    #ax.yaxis.grid(linestyle='-', linewidth=2)
    
    plt.show()