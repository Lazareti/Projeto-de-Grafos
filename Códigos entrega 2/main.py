from graph_model import load_graph_from_file, Graph
from ui import *

def main():
    print_title()
    g=None
    while True:
        print_menu()
        op=input("Opção: ")
        if op=="1":
            g=load_graph_from_file(input("Arquivo: "))
        elif op=="2" and g: handle_insert_remove_vertex(g)
        elif op=="3" and g: handle_insert_remove_edge(g)
        elif op=="4" and g: show_content(g)
        elif op=="5" and g: show_graph_text(g)
        elif op=="6" and g: test_connectivity(g)
        elif op=="7" and g: handle_shortest_path(g)
        elif op=="8" and g: handle_degrees_and_hubs(g)
        elif op=="9" and g: handle_eulerian(g)
        elif op=="10" and g: handle_coloring(g)
        elif op=="0": break
        else: print("Carregue um grafo primeiro!")

if __name__=="__main__":
    main()
