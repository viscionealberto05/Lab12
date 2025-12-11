import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self._soglia = 0

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        self.lista_nodi = DAO.getRifugi()

        #self.G.add_nodes_from(self.lista_nodi)

        self.lista_sentieri = DAO.getSentieri(year)

        for sentiero in self.lista_sentieri:
            difficolta = self.convertiDiff(sentiero)
            self.G.add_edge(sentiero.id_rifugio1, sentiero.id_rifugio2, weight=(difficolta * float(sentiero.distanza)))

    def convertiDiff(self, sentiero):
        if sentiero.difficolta == 'facile':
            return 1
        elif sentiero.difficolta == 'media':
            return 1.5
        elif sentiero.difficolta == 'difficile':
            return 2

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """

        minimo = 1000
        massimo = -1000

        for edge in self.G.edges(data=True):
            if edge[2]["weight"] <= minimo:
                minimo = edge[2]["weight"]

        for edge in self.G.edges(data=True):
            if edge[2]["weight"] >= massimo:
                massimo = edge[2]["weight"]

        return round(minimo,2), round(massimo,2)


    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        lista_maggiori = []
        lista_minori = []
        self._soglia = soglia

        for edge in self.G.edges(data=True):
            if edge[2]["weight"] <= soglia:
                lista_minori.append(round(edge[2]["weight"],2))
            else:
                lista_maggiori.append(round(edge[2]["weight"],2))

        return len(lista_minori), len(lista_maggiori)

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    """def cammino_minimo(self):
        #lista_nodi = []

        #for nodo in self.G.nodes():
        #    for nodo_vicino in self.G.neighbors(nodo):

        percorsi=[]

        best_overall_path = None
        best_overall_weight = float('inf')

        for start_node in self.G.nodes():
            path, weight = self.cammino_minimo_con_vincoli(self.G, start_node, self._soglia)
            if path is not None and weight < best_overall_weight:
                best_overall_path = path
                best_overall_weight = weight

        print("Percorso minimo globale:", best_overall_path)
        print("Peso:", best_overall_weight)

    def cammino_minimo_con_vincoli(self, G, start, soglia):
        best_path = None
        best_weight = float('inf')

        def dfs(current, path, weight):
            nonlocal best_path, best_weight

            # pruning: già peggio del migliore
            if weight > best_weight:
                return

            # se soddisfa i due vincoli → candidato
            if weight > soglia and len(path) >= 3:
                if weight < best_weight:
                    best_weight = weight
                    best_path = path.copy()

            # esplora i vicini
            for neighbor in G.neighbors(current):
                if neighbor not in path:  # evita cicli
                    edge_weight = G[current][neighbor]['weight']
                    dfs(neighbor, path + [neighbor], weight + edge_weight)

        dfs(start, [start], 0)
        return best_path, best_weight"""

    """def cammino_minimo(self):

        percorso_minimo = None
        self.percorsi = []

        for nodo in self.G.nodes():
            self.nodi_visti = []
            percorso = self.dfs(nodo,self.nodi_visti)
            if len(self.percorsi) != 0:
                for perc in self.percorsi:
                    if sorted(percorso["rifugi"]) == perc["rifugi"] and percorso["peso"] < perc["peso"]:
                        perc["rifugi"] = percorso["rifugi"]
            else:
                self.percorsi.append(percorso)

        print(self.percorsi)



    def dfs(self, nodo, nodi_visti):
        peso_percorso = 0
        for nodo_vicino in self.G.neighbors(nodo):
            if nodo_vicino in nodi_visti:
                pass
            else:
                for edge in self.G.edges(data=True):
                    if edge[0] == nodo and edge[1] == nodo_vicino:
                        peso_percorso += edge[2]["weight"]
                        nodi_visti.append(nodo_vicino)
                        self.dfs(nodo_vicino, nodi_visti)

        return {"rifugi":self.nodi_visti,"peso":peso_percorso}"""

    """def cammino_minimo(self):
        percorsi_validi = []
        soglia = self._soglia
        G = self.G

        def dfs(nodo_corrente, percorso_attuale, peso_attuale):
            for vicino in G.neighbors(nodo_corrente):
                if vicino not in percorso_attuale:
                    peso_arco = G[nodo_corrente][vicino]["weight"]

                    # Considera solo archi con peso >= soglia
                    if peso_arco >= soglia:
                        nuovo_percorso = percorso_attuale + [vicino]
                        nuovo_peso = peso_attuale + peso_arco

                        # Se ha almeno 2 archi (3 nodi), salva il percorso
                        if len(nuovo_percorso) >= 3:
                            percorsi_validi.append((nuovo_percorso, nuovo_peso))

                        # Continua DFS ricorsiva
                        dfs(vicino, nuovo_percorso, nuovo_peso)

        # Chiama DFS da ogni nodo di partenza
        for nodo in G.nodes():
            dfs(nodo, [nodo], 0)

        print(percorsi_validi)"""

    """def cammino_minimo(self):

        percorsi = []
        for nodo in self.G.nodes():
            percorso = {}
            edges = nx.bfs_edges(self.G,nodo)
            visited_nodes = []
            for u,v in edges:
                peso = self.G[u][v].get("weight")

                visited_nodes.append((v,peso))

            #while len(visited_nodes) > 0:


            if len(visited_nodes) >=3:
                for arco in visited_nodes:
                    flag = False
                    if arco[1] < self._soglia:
                        flag = True
                        break

                if flag == False:
                    percorso[nodo] = (visited_nodes)
                    percorsi.append(percorso)

            #FLAG che

        print(self._soglia)
        for percorso in percorsi:
            print(percorso)"""

    def cammino_minimo(self):

        percorsi = {}

        def peso_filtrato(u, v, d):
            w = d["weight"]
            return w if w > self._soglia else float("inf")

        for sorgente in self.G.nodes():

            # Percorsi pesati ignorando archi <= soglia
            cammini = nx.single_source_dijkstra_path(
                self.G,
                sorgente,
                weight=peso_filtrato
            )

            # filtro cammini con almeno 2 archi (≥ 3 nodi)
            validi = {
                dest: path
                for dest, path in cammini.items()
                if len(path) >= 3
            }

            if validi:
                percorsi[sorgente] = validi

        print("Soglia:", self._soglia)
        for s, paths in percorsi.items():
            print(f"Sorgente {s}:")
            for dest, path in paths.items():
                print(" ->", dest, path)


