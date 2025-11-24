from graph_model import Graph, compute_degrees, is_connected_undirected
from algorithms import dijkstra_shortest_path, eulerian_properties, greedy_coloring

def print_title():
    print("="*70)
    print("Otimização de Rotas Aéreas por Grafos")
    print("="*70)

def print_menu():
    print("\n1 Ler grafo")
    print("2 Inserir/Remover vértice")
    print("3 Inserir/Remover aresta")
    print("4 Mostrar conteúdo")
    print("5 Mostrar adjacência")
    print("6 Testar conexidade")
    print("7 Rota mais curta")
    print("8 Graus e hubs")
    print("9 Propriedades eulerianas")
    print("10 Coloração gulosa")
    print("0 Sair")

def handle_insert_remove_vertex(g:Graph):
    c=input("1 inserir / 2 remover: ")
    if c=="1":
        g.add_vertex(input("Vértice: "))
    elif c=="2":
        g.remove_vertex(input("Vértice: "))

def handle_insert_remove_edge(g:Graph):
    c=input("1 inserir / 2 remover: ")
    if c=="1":
        u=input("Origem: "); v=input("Destino: ")
        w=float(input("Peso: ") or 1)
        g.add_edge(u,v,w)
    else:
        g.remove_edge(input("Origem: "), input("Destino: "))

def show_content(g):
    print(g.vertices())
    print(g.edges())

def show_graph_text(g):
    for v in sorted(g.vertices()):
        print(v, ":", g.neighbors(v))

def test_connectivity(g):
    print("Conexo?" , is_connected_undirected(g))

def handle_shortest_path(g):
    o=input("Origem: "); d=input("Destino: ")
    dist,path=dijkstra_shortest_path(g,o,d)
    print(dist, path)

def handle_degrees_and_hubs(g):
    i,o=compute_degrees(g)
    for v in sorted(g.vertices()):
        print(v, i[v], o[v], i[v]+o[v])

def handle_eulerian(g):
    e,t=eulerian_properties(g)
    print("Euleriano:",e," Caminho Euleriano:",t)

def handle_coloring(g):
    print(greedy_coloring(g))
