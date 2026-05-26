# =============================================================================
# Universidade Presbiteriana Mackenzie
# Faculdade de Computação e Informática
# Disciplina: Teoria dos Grafos - Turma: 6G
# Prof. Dr. Ivan Carlos Alcântara de Oliveira
#
# Integrantes:
#   Gabriel Lazareti Cardoso - RA: 10417353
#   Hailo Neto               - RA: 10416839
#
# Descrição: Aplicação para mapeamento e análise de acesso do transporte
#            público aos centros esportivos de São Paulo, utilizando grafos
#            dirigidos com pesos (tempo de deslocamento em minutos).
#
# Histórico de alterações:
#   2025-02-12 | Gabriel Lazareti | Criação inicial - Projeto Parte 1
#   2025-02-12 | Hailo Neto       | Implementação das operações básicas de grafo
#   2026-05-25 | Gabriel Lazareti | Parte 3: Dijkstra, grau, euleriano, centralidade
# =============================================================================

import os
import heapq

ARQUIVO_GRAFO = "grafo.txt"


# =============================================================================
# ESTRUTURA DO GRAFO
# Representação: dicionário de listas de adjacência com pesos
# grafo[origem] = {destino: peso, ...}
# =============================================================================

def criar_grafo_vazio():
    """Cria e retorna um grafo vazio."""
    return {}


def inserir_vertice(grafo, vertice):
    """Insere um novo vértice no grafo, se ainda não existir."""
    if vertice in grafo:
        print(f"O vertice '{vertice}' ja existe.")
    else:
        grafo[vertice] = {}
        print(f"Vertice '{vertice}' inserido com sucesso.")


def inserir_aresta(grafo, origem, destino, peso=1):
    """Insere uma aresta dirigida de origem para destino com o peso informado."""
    if origem not in grafo:
        print(f"O vertice de origem '{origem}' nao existe.")
        return
    if destino not in grafo:
        print(f"O vertice de destino '{destino}' nao existe.")
        return
    if destino in grafo[origem]:
        print(f"A aresta {origem} -> {destino} ja existe.")
    else:
        grafo[origem][destino] = peso
        print(f"Aresta {origem} -> {destino} (peso {peso}) inserida com sucesso.")


def remover_vertice(grafo, vertice):
    """Remove um vértice e todas as arestas que o envolvem."""
    if vertice not in grafo:
        print(f"O vertice '{vertice}' nao existe.")
        return
    del grafo[vertice]
    for v in grafo:
        if vertice in grafo[v]:
            del grafo[v][vertice]
    print(f"Vertice '{vertice}' removido com sucesso.")


def remover_aresta(grafo, origem, destino):
    """Remove a aresta dirigida de origem para destino."""
    if origem not in grafo:
        print(f"O vertice de origem '{origem}' nao existe.")
        return
    if destino in grafo[origem]:
        del grafo[origem][destino]
        print(f"Aresta {origem} -> {destino} removida com sucesso.")
    else:
        print(f"A aresta {origem} -> {destino} nao existe.")


def mostrar_grafo(grafo):
    """Exibe o grafo no formato de lista de adjacência com pesos."""
    if not grafo:
        print("O grafo esta vazio.")
        return
    print("\nGrafo (lista de adjacencia com pesos):")
    for vertice in sorted(grafo.keys()):
        adjacentes = grafo[vertice]
        if adjacentes:
            vizinhos = ", ".join(
                f"{d}({adjacentes[d]}min)" for d in sorted(adjacentes)
            )
            print(f"  {vertice} -> {vizinhos}")
        else:
            print(f"  {vertice} -> vazio")


# =============================================================================
# LEITURA E GRAVAÇÃO EM ARQUIVO
# Formato do arquivo grafo.txt:
#   VERTICES:
#   <v1> <v2> ...
#
#   ARESTAS:
#   <origem> <destino> <peso>
# =============================================================================

def gravar_dados_no_arquivo(grafo, nome_arquivo=ARQUIVO_GRAFO):
    """Grava o grafo no arquivo no formato padrão da disciplina."""
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write("VERTICES:\n")
        arquivo.write(" ".join(sorted(grafo.keys())) + "\n\n")
        arquivo.write("ARESTAS:\n")
        for origem in sorted(grafo.keys()):
            for destino in sorted(grafo[origem]):
                peso = grafo[origem][destino]
                arquivo.write(f"{origem} {destino} {peso}\n")
    print(f"Dados gravados com sucesso no arquivo '{nome_arquivo}'.")


def ler_dados_do_arquivo(nome_arquivo=ARQUIVO_GRAFO):
    """Lê o grafo do arquivo e o carrega na memória."""
    grafo = criar_grafo_vazio()
    if not os.path.exists(nome_arquivo):
        print(f"O arquivo '{nome_arquivo}' nao existe. Um grafo vazio sera carregado.")
        return grafo

    secao = None
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            if linha.upper() == "VERTICES:":
                secao = "vertices"
                continue
            if linha.upper() == "ARESTAS:":
                secao = "arestas"
                continue
            if secao == "vertices":
                for vertice in linha.split():
                    if vertice not in grafo:
                        grafo[vertice] = {}
            elif secao == "arestas":
                partes = linha.split()
                if len(partes) >= 2:
                    origem, destino = partes[0], partes[1]
                    # Suporta arquivos com ou sem peso
                    peso = int(partes[2]) if len(partes) == 3 else 1
                    if origem not in grafo:
                        grafo[origem] = {}
                    if destino not in grafo:
                        grafo[destino] = {}
                    grafo[origem][destino] = peso

    print(f"Dados lidos com sucesso do arquivo '{nome_arquivo}'.")
    return grafo


def mostrar_conteudo_do_arquivo(nome_arquivo=ARQUIVO_GRAFO):
    """Exibe o conteúdo bruto do arquivo grafo.txt."""
    if not os.path.exists(nome_arquivo):
        print(f"O arquivo '{nome_arquivo}' nao existe.")
        return
    print(f"\nConteudo do arquivo '{nome_arquivo}':\n")
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        print(arquivo.read())


# =============================================================================
# CONECTIVIDADE (mantida e adaptada do Projeto 2)
# =============================================================================

def busca_profundidade(grafo, vertice, visitados, pilha=None):
    """DFS iterativa usada no algoritmo de Kosaraju."""
    visitados.add(vertice)
    for vizinho in grafo[vertice]:
        if vizinho not in visitados:
            busca_profundidade(grafo, vizinho, visitados, pilha)
    if pilha is not None:
        pilha.append(vertice)


def coletar_componente(grafo, vertice, visitados, componente):
    """Coleta todos os vértices de uma componente via DFS."""
    visitados.add(vertice)
    componente.append(vertice)
    for vizinho in grafo[vertice]:
        if vizinho not in visitados:
            coletar_componente(grafo, vizinho, visitados, componente)


def inverter_grafo(grafo):
    """Retorna o grafo transposto (arestas invertidas)."""
    grafo_invertido = {v: {} for v in grafo}
    for origem in grafo:
        for destino, peso in grafo[origem].items():
            grafo_invertido[destino][origem] = peso
    return grafo_invertido


def componentes_fortemente_conexas(grafo):
    """Algoritmo de Kosaraju para encontrar SCCs."""
    visitados = set()
    pilha = []
    for vertice in grafo:
        if vertice not in visitados:
            busca_profundidade(grafo, vertice, visitados, pilha)
    grafo_invertido = inverter_grafo(grafo)
    visitados = set()
    componentes = []
    while pilha:
        vertice = pilha.pop()
        if vertice not in visitados:
            componente = []
            coletar_componente(grafo_invertido, vertice, visitados, componente)
            componentes.append(sorted(componente))
    return componentes


def existe_caminho(grafo, origem, destino):
    """Verifica se existe caminho dirigido de origem até destino."""
    if origem == destino:
        return True
    visitados = set()
    pilha = [origem]
    while pilha:
        atual = pilha.pop()
        if atual == destino:
            return True
        if atual not in visitados:
            visitados.add(atual)
            for vizinho in grafo[atual]:
                if vizinho not in visitados:
                    pilha.append(vizinho)
    return False


def grafo_nao_direcionado(grafo):
    """Converte o grafo dirigido em não dirigido para verificar fraca conexidade."""
    grafo_nd = {v: set() for v in grafo}
    for origem in grafo:
        for destino in grafo[origem]:
            grafo_nd[origem].add(destino)
            grafo_nd[destino].add(origem)
    return grafo_nd


def eh_conexo_nao_direcionado(grafo_nd):
    """Verifica se o grafo não dirigido é conexo via DFS."""
    if not grafo_nd:
        return True
    visitados = set()
    pilha = [next(iter(grafo_nd))]
    while pilha:
        atual = pilha.pop()
        if atual not in visitados:
            visitados.add(atual)
            for vizinho in grafo_nd[atual]:
                if vizinho not in visitados:
                    pilha.append(vizinho)
    return len(visitados) == len(grafo_nd)


def classificar_conexidade(grafo):
    """Classifica o grafo como: Fortemente, Unilateralmente, Fracamente ou Desconexo."""
    if not grafo:
        return "Grafo vazio"
    componentes = componentes_fortemente_conexas(grafo)
    if len(componentes) == 1:
        return "Fortemente conexo"
    vertices = list(grafo.keys())
    unilateral = True
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            v1, v2 = vertices[i], vertices[j]
            if not (existe_caminho(grafo, v1, v2) or existe_caminho(grafo, v2, v1)):
                unilateral = False
                break
        if not unilateral:
            break
    if unilateral:
        return "Unilateralmente conexo"
    if eh_conexo_nao_direcionado(grafo_nao_direcionado(grafo)):
        return "Fracamente conexo"
    return "Desconexo"


def grafo_reduzido(grafo):
    """Constrói o grafo reduzido (condensação) das SCCs."""
    componentes = componentes_fortemente_conexas(grafo)
    mapa = {}
    for i, comp in enumerate(componentes):
        for v in comp:
            mapa[v] = i
    reduzido = {i: set() for i in range(len(componentes))}
    for origem in grafo:
        for destino in grafo[origem]:
            c_orig, c_dest = mapa[origem], mapa[destino]
            if c_orig != c_dest:
                reduzido[c_orig].add(c_dest)
    return componentes, reduzido


def mostrar_conexidade_e_reduzido(grafo):
    """Exibe a conexidade do grafo, suas SCCs e o grafo reduzido."""
    if not grafo:
        print("O grafo esta vazio.")
        return
    print(f"\nConexidade do grafo: {classificar_conexidade(grafo)}")
    componentes, reduzido = grafo_reduzido(grafo)
    print("\nComponentes fortemente conexas:")
    for i, comp in enumerate(componentes):
        print(f"  C{i}: {', '.join(comp)}")
    print("\nGrafo reduzido:")
    for i in sorted(reduzido.keys()):
        destinos = sorted(reduzido[i])
        if destinos:
            print(f"  C{i} -> {', '.join(f'C{d}' for d in destinos)}")
        else:
            print(f"  C{i} -> vazio")


# =============================================================================
# PARTE 3 - TÉCNICA PRINCIPAL: DIJKSTRA
# Encontra o menor caminho (tempo) entre dois pontos da rede de transporte.
# Complexidade: O((V + E) log V) com heap binário.
# =============================================================================

def dijkstra(grafo, origem):
    """
    Algoritmo de Dijkstra para menor caminho a partir de uma origem.
    Retorna:
      distancias: dicionário {vertice: custo_minimo}
      anteriores: dicionário {vertice: vertice_anterior} para reconstrução do caminho
    """
    distancias = {v: float('inf') for v in grafo}
    distancias[origem] = 0
    anteriores = {v: None for v in grafo}
    heap = [(0, origem)]  # (custo, vertice)

    while heap:
        custo_atual, atual = heapq.heappop(heap)

        # Ignora se já encontramos caminho menor
        if custo_atual > distancias[atual]:
            continue

        for vizinho, peso in grafo[atual].items():
            novo_custo = custo_atual + peso
            if novo_custo < distancias[vizinho]:
                distancias[vizinho] = novo_custo
                anteriores[vizinho] = atual
                heapq.heappush(heap, (novo_custo, vizinho))

    return distancias, anteriores


def reconstruir_caminho(anteriores, origem, destino):
    """Reconstrói o caminho do destino até a origem percorrendo os predecessores."""
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]
    caminho.reverse()
    # Verifica se o caminho realmente parte da origem
    if caminho and caminho[0] == origem:
        return caminho
    return []


def menor_caminho(grafo):
    """
    Menu interativo: solicita origem e destino e exibe a rota mais rápida
    usando Dijkstra, com o tempo total de viagem.
    """
    if not grafo:
        print("O grafo esta vazio.")
        return

    print("\n--- Menor Caminho (Rota mais rapida) via Dijkstra ---")
    origem = input("Digite o ponto de origem: ").strip()
    destino = input("Digite o ponto de destino: ").strip()

    if origem not in grafo:
        print(f"Vertice '{origem}' nao encontrado no grafo.")
        return
    if destino not in grafo:
        print(f"Vertice '{destino}' nao encontrado no grafo.")
        return

    distancias, anteriores = dijkstra(grafo, origem)

    if distancias[destino] == float('inf'):
        print(f"\nNao existe caminho de '{origem}' ate '{destino}'.")
        return

    caminho = reconstruir_caminho(anteriores, origem, destino)
    print(f"\nRota mais rapida de '{origem}' ate '{destino}':")
    print(f"  Percurso : {' -> '.join(caminho)}")
    print(f"  Tempo total: {distancias[destino]} minutos")


# =============================================================================
# PARTE 3 - CARACTERÍSTICA 1: GRAU DOS VÉRTICES
# Identifica os hubs mais conectados da rede de transporte.
# Grau de entrada = linhas que chegam; Grau de saída = linhas que partem.
# =============================================================================

def analisar_graus(grafo):
    """
    Calcula e exibe o grau de entrada e saída de cada vértice.
    Destaca os vértices com maior e menor conectividade.
    """
    if not grafo:
        print("O grafo esta vazio.")
        return

    grau_saida  = {v: len(grafo[v]) for v in grafo}
    grau_entrada = {v: 0 for v in grafo}

    for origem in grafo:
        for destino in grafo[origem]:
            grau_entrada[destino] += 1

    grau_total = {v: grau_entrada[v] + grau_saida[v] for v in grafo}

    print("\n--- Analise de Grau dos Vertices ---")
    print(f"{'Vertice':<35} {'Entrada':>8} {'Saida':>7} {'Total':>7}")
    print("-" * 60)
    for v in sorted(grafo.keys()):
        print(f"  {v:<33} {grau_entrada[v]:>8} {grau_saida[v]:>7} {grau_total[v]:>7}")

    hub = max(grau_total, key=grau_total.get)
    isolado = min(grau_total, key=grau_total.get)
    print(f"\n  Hub principal (maior grau total) : {hub} (grau {grau_total[hub]})")
    print(f"  Vertice menos conectado          : {isolado} (grau {grau_total[isolado]})")


# =============================================================================
# PARTE 3 - CARACTERÍSTICA 2: VERIFICAÇÃO EULERIANA
# Um grafo dirigido tem circuito euleriano se:
#   - É fortemente conexo E grau_entrada == grau_saida para todo vértice.
# Tem caminho euleriano se:
#   - Exatamente 1 vértice com grau_saida - grau_entrada = 1 (início)
#     e 1 vértice com grau_entrada - grau_saida = 1 (fim).
# =============================================================================

def verificar_euleriano(grafo):
    """
    Verifica se o grafo admite circuito ou percurso euleriano
    e explica o resultado no contexto do problema de transporte.
    """
    if not grafo:
        print("O grafo esta vazio.")
        return

    grau_saida  = {v: len(grafo[v]) for v in grafo}
    grau_entrada = {v: 0 for v in grafo}
    for origem in grafo:
        for destino in grafo[origem]:
            grau_entrada[destino] += 1

    # Vértices com graus desbalanceados
    inicio_candidatos = []   # grau_saida - grau_entrada == 1
    fim_candidatos    = []   # grau_entrada - grau_saida == 1
    desbalanceados    = []   # diferença > 1

    for v in grafo:
        diff = grau_saida[v] - grau_entrada[v]
        if diff == 1:
            inicio_candidatos.append(v)
        elif diff == -1:
            fim_candidatos.append(v)
        elif diff != 0:
            desbalanceados.append(v)

    conexo = classificar_conexidade(grafo) == "Fortemente conexo"

    print("\n--- Verificacao Euleriana ---")

    if conexo and not desbalanceados and not inicio_candidatos and not fim_candidatos:
        print("  Resultado: CIRCUITO EULERIANO existente.")
        print("  Interpretacao: e possivel criar uma rota circular que percorre")
        print("  todas as conexoes de transporte exatamente uma vez e retorna ao inicio.")

    elif (len(inicio_candidatos) == 1 and len(fim_candidatos) == 1
          and not desbalanceados):
        print("  Resultado: CAMINHO EULERIANO existente (nao e circuito).")
        print(f"  Inicio sugerido : {inicio_candidatos[0]}")
        print(f"  Fim sugerido    : {fim_candidatos[0]}")
        print("  Interpretacao: existe uma rota que percorre todas as conexoes")
        print("  exatamente uma vez, mas sem retornar ao ponto de partida.")

    else:
        print("  Resultado: NAO e Euleriano.")
        print(f"  Vertices fortemente conexos: {'Sim' if conexo else 'Nao'}")
        print(f"  Vertices desbalanceados    : {len(desbalanceados) + len(inicio_candidatos) + len(fim_candidatos)}")
        print("  Interpretacao: a rede de transporte nao permite percorrer todas")
        print("  as conexoes exatamente uma vez em uma unica viagem.")


# =============================================================================
# PARTE 3 - CARACTERÍSTICA 3: CENTRALIDADE DE PROXIMIDADE (Closeness Centrality)
# Mede o quão central um ponto é na rede com base na soma dos menores caminhos.
# Pontos com alta centralidade têm melhor acesso geral à rede de transporte.
# Centralidade = (n-1) / soma_das_distancias  (normalizada)
# =============================================================================

def centralidade_proximidade(grafo):
    """
    Calcula a centralidade de proximidade de cada vértice usando Dijkstra.
    Vértices com alta centralidade são os de melhor acesso ao sistema de transporte.
    """
    if not grafo:
        print("O grafo esta vazio.")
        return

    n = len(grafo)
    centralidade = {}

    for origem in grafo:
        distancias, _ = dijkstra(grafo, origem)
        alcancaveis = [d for d in distancias.values() if d != float('inf') and d > 0]
        if alcancaveis:
            # Fórmula normalizada para grafos desconexos
            centralidade[origem] = len(alcancaveis) / sum(alcancaveis)
        else:
            centralidade[origem] = 0.0

    # Ordena do mais central para o menos central
    ranking = sorted(centralidade.items(), key=lambda x: x[1], reverse=True)

    print("\n--- Centralidade de Proximidade (Acesso a Rede) ---")
    print(f"  {'Posicao':<8} {'Vertice':<35} {'Centralidade':>12}")
    print("  " + "-" * 58)
    for pos, (vertice, valor) in enumerate(ranking, start=1):
        print(f"  {pos:<8} {vertice:<35} {valor:>12.6f}")

    print(f"\n  Ponto de MELHOR acesso a rede : {ranking[0][0]}")
    print(f"  Ponto de PIOR  acesso a rede  : {ranking[-1][0]}")
    print("\n  Interpretacao: pontos com maior centralidade estao mais 'proximos'")
    print("  dos demais pontos da rede e representam os melhores pontos de")
    print("  partida para acessar centros esportivos via transporte publico.")


# =============================================================================
# MENU PRINCIPAL
# =============================================================================

def mostrar_menu():
    print("\n" + "=" * 55)
    print("  MAPEAMENTO DE ACESSO DO TRANSPORTE PUBLICO AOS")
    print("       CENTROS ESPORTIVOS DE SAO PAULO")
    print("=" * 55)
    print("  a) Ler dados do arquivo grafo.txt")
    print("  b) Gravar dados no arquivo grafo.txt")
    print("  c) Inserir vertice")
    print("  d) Inserir aresta")
    print("  e) Remover vertice")
    print("  f) Remover aresta")
    print("  g) Mostrar conteudo do arquivo")
    print("  h) Mostrar grafo")
    print("  i) Apresentar conexidade do grafo e grafo reduzido")
    print("  j) Menor caminho entre dois pontos (Dijkstra)")
    print("  k) Analisar grau dos vertices (hubs da rede)")
    print("  l) Verificar propriedade Euleriana")
    print("  m) Centralidade de proximidade (acesso a rede)")
    print("  n) Encerrar a aplicacao")
    print("=" * 55)


def main():
    grafo = criar_grafo_vazio()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opcao: ").strip().lower()

        if opcao == "a":
            grafo = ler_dados_do_arquivo()

        elif opcao == "b":
            gravar_dados_no_arquivo(grafo)

        elif opcao == "c":
            vertice = input("Digite o nome do vertice: ").strip()
            if vertice:
                inserir_vertice(grafo, vertice)
            else:
                print("Nome de vertice invalido.")

        elif opcao == "d":
            origem  = input("Digite o vertice de origem: ").strip()
            destino = input("Digite o vertice de destino: ").strip()
            peso_str = input("Digite o peso (tempo em minutos, padrao=1): ").strip()
            peso = int(peso_str) if peso_str.isdigit() else 1
            if origem and destino:
                inserir_aresta(grafo, origem, destino, peso)
            else:
                print("Vertices invalidos.")

        elif opcao == "e":
            vertice = input("Digite o vertice a ser removido: ").strip()
            if vertice:
                remover_vertice(grafo, vertice)
            else:
                print("Nome de vertice invalido.")

        elif opcao == "f":
            origem  = input("Digite o vertice de origem da aresta: ").strip()
            destino = input("Digite o vertice de destino da aresta: ").strip()
            if origem and destino:
                remover_aresta(grafo, origem, destino)
            else:
                print("Vertices invalidos.")

        elif opcao == "g":
            mostrar_conteudo_do_arquivo()

        elif opcao == "h":
            mostrar_grafo(grafo)

        elif opcao == "i":
            mostrar_conexidade_e_reduzido(grafo)

        elif opcao == "j":
            menor_caminho(grafo)

        elif opcao == "k":
            analisar_graus(grafo)

        elif opcao == "l":
            verificar_euleriano(grafo)

        elif opcao == "m":
            centralidade_proximidade(grafo)

        elif opcao == "n":
            print("Encerrando a aplicacao...")
            break

        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    main()