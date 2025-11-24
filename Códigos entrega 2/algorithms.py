from typing import Dict, List, Tuple, Optional
import heapq
from graph_model import Graph, compute_degrees, all_neighbors_undirected

def eulerian_properties(g: Graph):
    in_deg, out_deg = compute_degrees(g)
    verts = [v for v in g.vertices() if in_deg[v] + out_deg[v] > 0]
    start=end=0
    for v in verts:
        if in_deg[v]==out_deg[v]: continue
        elif out_deg[v]==in_deg[v]+1: start+=1
        elif in_deg[v]==out_deg[v]+1: end+=1
        else: return False, False
    if start==0 and end==0: return True, False
    if start==1 and end==1: return False, True
    return False, False

def greedy_coloring(g: Graph):
    color = {}
    for v in sorted(g.vertices()):
        used=set(color[u] for u in all_neighbors_undirected(g,v) if u in color)
        c=1
        while c in used: c+=1
        color[v]=c
    return color

def dijkstra_shortest_path(g: Graph, source: str, target: str):
    if source not in g.adj or target not in g.adj:
        return float('inf'), []
    dist={v:float('inf') for v in g.vertices()}
    prev={v:None for v in g.vertices()}
    dist[source]=0
    heap=[(0,source)]
    while heap:
        cd,u=heapq.heappop(heap)
        if cd>dist[u]: continue
        if u==target: break
        for v,w in g.neighbors(u):
            nd=cd+w
            if nd<dist[v]:
                dist[v]=nd; prev[v]=u
                heapq.heappush(heap,(nd,v))
    if dist[target]==float('inf'): return float('inf'), []
    path=[]; cur=target
    while cur: path.append(cur); cur=prev[cur]
    return dist[target], list(reversed(path))
