import matplotlib.pyplot as plt
import networkx as nx
#reference
#https://networkx.github.io/documentation/networkx-2.2/auto_examples/index.html#drawing
def plot(graph, weights, monitors, lm, pos=None):
    G = nx.Graph()
    Nodes=[]
    monitorNodes = []
    for edge, w in weights.items():
        G.add_edge(edge.node1.id, edge.node2.id , weight=0.1)
        if edge.node2.id not in Nodes:
            Nodes.append(edge.node2.id)
        if edge.node1.id not in Nodes:
            Nodes.append(edge.node1.id)
    for edge in lm:
        G.add_edge(edge.node1.id, edge.node2.id , weight=1.0)
    
    for m in monitors:
        monitorNodes.append(m.id)
    
    
    lm = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
    l = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]
    if pos is None:
        pos = nx.spring_layout(G)
        
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=99, nodelist=Nodes, node_color="black", alpha=0.5)
    nx.draw_networkx_nodes(G, pos, node_size=100, nodelist=monitorNodes, node_color='red')
    nx.draw_networkx_edges(G, pos, edgelist=l, width=1, edge_color="black")
    nx.draw_networkx_edges(G, pos, edgelist=lm,
                       width=2, edge_color="red")
    
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    
    plt.axis('off')
    plt.show()
    return pos