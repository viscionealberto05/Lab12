import networkx as nx
from database.dao import DAO
from matplotlib import pyplot as plt

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        #self.lista_nodi = DAO.getRifugi()

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

        for edge in self.G.edges(data=True):
            if edge[2]["weight"] <= soglia:
                lista_minori.append(round(edge[2]["weight"],2))
            else:
                lista_maggiori.append(round(edge[2]["weight"],2))

        return len(lista_minori), len(lista_maggiori)

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    def cammino_minimo(self):
        pos = nx.planar_layout(self.G)
        nx.draw(self.G, pos)
        labels = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)