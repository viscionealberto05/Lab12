import networkx as nx
from operator import itemgetter
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
            if edge[2]["weight"] < minimo:
                minimo = edge[2]["weight"]

        for edge in self.G.edges(data=True):
            if edge[2]["weight"] > massimo:
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
            if edge[2]["weight"] < soglia:
                lista_minori.append(round(edge[2]["weight"],2))
            elif edge[2]["weight"] > soglia:
                lista_maggiori.append(round(edge[2]["weight"],2))

        return len(lista_minori), len(lista_maggiori)


    def cammino_minimo(self):

        #Provo ad appoggiarmi ad un algoritmo AP-SP, per ricercare il percorso minimo
        #cioè più corto (rispettando le indicazioni dell'esercizio) tra qualunque paio di vertici

        #deve venirmi restuito sia il peso complessivo del percorso minimo, che la sequenza di nodi

        #ciascun arco all'interno del potenziale percorso con peso minimo deve avere peso superiore alla soglia
        #considero solo i percorsi che hanno almeno 3 nodi



            percorsi_minimi = {}  # dizionario finale: sorgente → destinazione → percorso

            # Funzione peso che filtra gli archi così che l'algoritmo possa escludere i percorsi che li contengono

            for edge in self.G.edges(data=True):
                if edge[2]["weight"] <= self._soglia:
                    edge[2]["weight"] = float("inf")



            # Eseguo Dijkstra da ogni nodo

            for nodo_sorgente in self.G.nodes():

                # Questo dà il dizionario di cammini minimi verso ciascun nodo raggiungibile, il nodo di destinazione è la chiave
                #il valore è una lista di tutti i nodi attraversati
                cammini = nx.single_source_dijkstra_path(
                    self.G, nodo_sorgente, weight="weight"
                )

                # Questo dà il dizionario che ha per chiave il nodo di destinazione e per valore il costo del cammino
                costo_cammino = nx.single_source_dijkstra_path_length(
                    self.G, nodo_sorgente, weight="weight"
                )

                validi = {}

                #Una volta ottenuti i cammini minimi del singolo nodo, vado ad escludere quelli
                #con meno di 3 nodi e che hanno archi sottosoglia (la cui distanza è stata volutamente posta a inf
                #nella scrematura iniziale prima del Dijkstra)

                #Creo quindi un dizionario "validi", ne esiste uno per ogni nodo sorgente, la chiave sarà la
                #destinazione del percorso minimo, il valore sarà una tupla composta da due elementi:
                # 0. lista di nodi attraversati per raggiungere la destinazione, recuperato dal dizionario "cammini" output del dijkstra per il singolo nodo
                # 1. costo (o peso) complessivo del percorso per quella specifica destinazione, ottenuto dal dizionario "costo_cammino" output del dijkstra, con chiave la destinazione stessa

                for destinazione, path in cammini.items():

                    # Deve contenere almeno 3 nodi
                    if len(path) < 3:
                        continue

                    # Il costo deve essere finito (cioè il cammino non passa da archi sotto soglia)
                    costo = costo_cammino[destinazione]
                    if costo == float("inf"):
                        continue

                    # Salvo il cammino valido
                    validi[destinazione] = (path, costo)

                #Prima di uscire dal ciclo for che itera sui nodi come sorgenti, mi accerto che ci sia almeno una destinazione
                #valida (con annesso percorso e costo) per il singolo nodo, se il controllo viene superato allora associo, nel
                #dizionario "percorsi_minimi", alla chiave "nodo_sorgente", il dizionario "validi", all'interno del quale
                #sono contenuti come chiavi tutti i nodi raggiungibili e come valori tutte tuple contenenti lista dei percorsi
                #e costo complessivo

                #STRUTTURA:
                #{ nodo_sorgente_1 : { nodo_dest_1 : ( [ np1,np2,... ], $$ ), nodo_dest_2 : ([],$),...} , nodo_sorgente_2 : { nd : ([],$), ... }, ... }

                if len(validi.keys()) != 0:
                    percorsi_minimi[nodo_sorgente] = validi

            #Una volta uscito dal ciclo for ho una struttura dati con tutti i percorsi minimi che soddisfano i vincoli
            #richiesti dall'esercizio per ciascun nodo sorgente

            for nodo_sorgente, validi in percorsi_minimi.items():
                # ordina validi per costo crescente (secondo elemento della tupla)
                validi_ordinati = dict(sorted(validi.items(), key=lambda item: item[1][1]))
                #item[1][1] indica che all'interno di "validi.items" considero il valore (non la chiave), e siccome questo valore è una tupla, il secondo elemento di questa (il costo/peso)

                #cambio dunque i valori assegnati alle chiavi nel dizionario di partenza
                percorsi_minimi[nodo_sorgente] = validi_ordinati

            for key in percorsi_minimi:
                print(f"{key} ha {percorsi_minimi[key]}")

            #Costruisco ora un algoritmo in grado di trovare tra tutti i percorsi minimi dei miei nodi sorgente, quello
            #che in assoluto abbia costo minore (possono essere più di uno con lo stesso costo)

            #Inizializzo una variabile per il costo minimo, che verrà costantemente aggiornata finchè non si troverà il percorso che tra tutti
            #avrà il costo più basso in assoluto

            min_costo = float("inf")

            for sorgente, validi in percorsi_minimi.items():
                for dest, (path, costo) in validi.items():
                    if costo < min_costo:
                        min_costo = costo

            percorsi_minimi_assoluti = []

            for sorgente, validi in percorsi_minimi.items():
                for dest, (path, costo) in validi.items():
                    if costo == min_costo:
                        percorsi_minimi_assoluti.append([sorgente, dest, path, costo])

            print(f"Costo minimo assoluto: {min_costo}")
            for sorgente, dest, path, costo in percorsi_minimi_assoluti:
                print(f"Sorgente: {sorgente}, Destinazione: {dest}, Percorso: {path}, Costo: {costo}")

            #Rimuovo i percorsi duplicati
            percorsi_minimi_non_duplicati = []
            for sorgente, dest, path, costo in percorsi_minimi_assoluti:
                for sorgente2, dest2, path2, costo2 in percorsi_minimi_assoluti:

                    #se osservo che la partenza di un percorso coincide con la destinazione dell'altro allora
                    #vado direttamente al percorso successivo perchè ho un duplicato

                    if sorgente == dest2:
                        break
                    else:
                        percorsi_minimi_non_duplicati.append([sorgente, dest, path, costo])



            for i in range(len(percorsi_minimi_non_duplicati)):
                for rifugio in self.lista_nodi:
                    if rifugio.id == percorsi_minimi_assoluti[i][0]:
                        percorsi_minimi_assoluti[i][0] = rifugio
                    if rifugio.id == percorsi_minimi_assoluti[i][1]:
                        percorsi_minimi_assoluti[i][1] = rifugio

            return percorsi_minimi_non_duplicati

    def cammino_minimo_recursive(self):
        pass