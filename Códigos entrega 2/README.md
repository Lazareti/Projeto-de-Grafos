# Projeto de Grafos – Parte 2 (Versão Modular)

Este projeto implementa análise de rotas aéreas brasileiras utilizando **Teoria dos Grafos**.

## 📁 Estrutura do Projeto

```
src/
 ├── graph_model.py   # Estrutura do grafo e operações básicas
 ├── algorithms.py    # Dijkstra, Euleriano, Coloração
 ├── ui.py            # Funções de interação do menu
 └── main.py          # Arquivo principal (loop do programa)
docs/
 └── Relatorio_Parte2.txt
```

## ▶️ Como executar

1. Instale Python 3.10+
2. Coloque seu arquivo `grafo_aeroportos_60.txt` na raiz
3. Rode:

```
python src/main.py
```

## Funcionalidades

- Carregar grafo
- Inserir/remover vértices e arestas
- Mostrar adjacência
- Testar conexidade
- Caminho mínimo (Dijkstra)
- Graus e hubs
- Propriedades eulerianas
- Coloração gulosa
