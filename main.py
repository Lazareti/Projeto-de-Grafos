import networkx as nx
import matplotlib.pyplot as plt

class GrafoApp:
    def __init__(self):
        self.G = nx.DiGraph()

    # 1. Ler grafo.txt
    def ler_grafo(self, arquivo="grafo.txt"):
        with open(arquivo, "r", encoding="utf-8") as f:
            linhas = f.read().splitlines()
        n = int(linhas[1])  # número de vértices
        idx = 2
        for i in range(n):
            parte = linhas[idx].split()
            v = int(parte[0])
            nome = " ".join(parte[1:]).strip('"')
            self.G.add_node(v, label=nome)
            idx += 1
        m = int(linhas[idx]); idx += 1
        for i in range(m):
            u, v, w = linhas[idx].split()
            self.G.add_edge(int(u), int(v), weight=int(w))
            idx += 1
        print(f"Grafo carregado com {self.G.number_of_nodes()} vértices e {self.G.number_of_edges()} arestas.")

    # 1b. Gravar grafo.txt
    def gravar_grafo(self, arquivo="grafo_out.txt"):
        linhas = ["6", str(self.G.number_of_nodes())]
        for v, dados in self.G.nodes(data=True):
            nome = dados.get("label", str(v))
            linhas.append(f'{v} "{nome}" 0')
        linhas.append(str(self.G.number_of_edges()))
        for u, v, dados in self.G.edges(data=True):
            linhas.append(f"{u} {v} {dados.get('weight',1)}")
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas))
        print(f"Grafo gravado em {arquivo}")

    # 2. Inserir vértice
    def inserir_vertice(self, v, nome):
        self.G.add_node(v, label=nome)
        print(f"Vértice {v} - {nome} inserido.")

    # 2b. Remover vértice
    def remover_vertice(self, v):
        if self.G.has_node(v):
            self.G.remove_node(v)
            print(f"Vértice {v} removido.")
        else:
            print("Vértice não encontrado.")

    # 3. Inserir aresta
    def inserir_aresta(self, u, v, w=1):
        self.G.add_edge(u, v, weight=w)
        print(f"Aresta {u}->{v} inserida (peso {w}).")

    # 3b. Remover aresta
    def remover_aresta(self, u, v):
        if self.G.has_edge(u, v):
            self.G.remove_edge(u, v)
            print(f"Aresta {u}->{v} removida.")
        else:
            print("Aresta não encontrada.")

    # 4. Mostrar conteúdo
    def mostrar_conteudo(self):
        print("Vértices:", self.G.nodes(data=True))
        print("Arestas:", self.G.edges(data=True))

    # 5. Mostrar grafo
    def mostrar_grafo(self):
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, node_color="lightblue", edgecolors="k")
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)
        plt.show()

    # 6. Testar conexidade/reduzido
    def testar_conexidade(self):
        if nx.is_weakly_connected(self.G):
            print("O grafo é fracamente conexo.")
        else:
            print("O grafo NÃO é conexo.")

        # grafo reduzido = remover arestas paralelas redundantes
        H = nx.DiGraph()
        for u, v, data in self.G.edges(data=True):
            if not H.has_edge(u, v):
                H.add_edge(u, v, weight=data['weight'])
        print(f"Grafo reduzido: {H.number_of_nodes()} vértices, {H.number_of_edges()} arestas.")

# -------------------------
# Menu
# -------------------------
def menu():
    app = GrafoApp()
    while True:
        print("\n--- MENU ---")
        print("1 - Ler Grafo (grafo.txt)")
        print("2 - Gravar Grafo (grafo_out.txt)")
        print("3 - Inserir Vértice")
        print("4 - Remover Vértice")
        print("5 - Inserir Aresta")
        print("6 - Remover Aresta")
        print("7 - Mostrar Conteúdo")
        print("8 - Mostrar Grafo")
        print("9 - Testar Conexidade/Reduzido")
        print("0 - Encerrar")

        op = input("Escolha: ")
        if op == "1":
            app.ler_grafo("grafo_aeroportos_60.txt")
        elif op == "2":
            app.gravar_grafo()
        elif op == "3":
            v = int(input("ID do vértice: "))
            nome = input("Nome do vértice: ")
            app.inserir_vertice(v, nome)
        elif op == "4":
            v = int(input("ID do vértice: "))
            app.remover_vertice(v)
        elif op == "5":
            u = int(input("Origem: "))
            v = int(input("Destino: "))
            w = int(input("Peso: "))
            app.inserir_aresta(u, v, w)
        elif op == "6":
            u = int(input("Origem: "))
            v = int(input("Destino: "))
            app.remover_aresta(u, v)
        elif op == "7":
            app.mostrar_conteudo()
        elif op == "8":
            app.mostrar_grafo()
        elif op == "9":
            app.testar_conexidade()
        elif op == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
