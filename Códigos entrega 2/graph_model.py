from typing import Dict, List, Tuple, Optional

class Graph:
    def __init__(self, directed: bool = True) -> None:
        self.directed = directed
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def add_vertex(self, v: str) -> None:
        if v not in self.adj:
            self.adj[v] = []

    def remove_vertex(self, v: str) -> None:
        if v not in self.adj:
            print(f"Vértice '{v}' não existe.")
            return
        self.adj.pop(v)
        for u in list(self.adj.keys()):
            self.adj[u] = [(w, wt) for (w, wt) in self.adj[u] if w != v]
        print(f"Vértice '{v}' removido com sucesso.")

    def add_edge(self, u: str, v: str, weight: float = 1.0) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))
        print(f"Aresta '{u} -> {v}' com peso {weight} adicionada.")

    def remove_edge(self, u: str, v: str) -> None:
        if u not in self.adj:
            print(f"Vértice de origem '{u}' não existe.")
            return
        original_len = len(self.adj[u])
        self.adj[u] = [(w, wt) for (w, wt) in self.adj[u] if w != v]
        if len(self.adj[u]) < original_len:
            print(f"Aresta '{u} -> {v}' removida.")
        else:
            print(f"Aresta '{u} -> {v}' não encontrada.")
        if not self.directed and v in self.adj:
            self.adj[v] = [(w, wt) for (w, wt) in self.adj[v] if w != u]

    def vertices(self) -> List[str]:
        return list(self.adj.keys())

    def edges(self) -> List[Tuple[str, str, float]]:
        result = []
        for u, vizinhos in self.adj.items():
            for v, w in vizinhos:
                result.append((u, v, w))
        return result

    def neighbors(self, v: str) -> List[Tuple[str, float]]:
        return self.adj.get(v, [])

def load_graph_from_file(filename: str) -> Optional['Graph']:
    g = Graph(directed=True)
    try:
        with open(filename, encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    u, v = parts[0], parts[1]
                    weight = float(parts[2].replace(",", ".")) if len(parts) >= 3 else 1.0
                    g.add_edge(u, v, weight)
        print(f"Grafo carregado de '{filename}'")
        return g
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return None

def compute_degrees(g: Graph):
    out_degree = {v: len(g.neighbors(v)) for v in g.vertices()}
    in_degree = {v: 0 for v in g.vertices()}
    for u, l in g.adj.items():
        for v, _ in l: in_degree[v] += 1
    return in_degree, out_degree

def is_connected_undirected(g: Graph) -> bool:
    verts = g.vertices()
    if not verts: return True
    visited = set()
    stack = [verts[0]]
    while stack:
        v = stack.pop()
        if v in visited: continue
        visited.add(v)
        for w,_ in g.neighbors(v):
            if w not in visited: stack.append(w)
        for u, l in g.adj.items():
            for w,_ in l:
                if w == v and u not in visited:
                    stack.append(u)
    return len(visited)==len(verts)

def all_neighbors_undirected(g:Graph, v:str):
    s = set()
    for w,_ in g.neighbors(v): s.add(w)
    for u,l in g.adj.items():
        for w,_ in l:
            if w==v: s.add(u)
    return list(s)
