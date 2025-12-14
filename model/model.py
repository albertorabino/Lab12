import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO

        self.G = nx.Graph()

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.G.clear()
        rifugi = DAO.cerca_rifugi(year)

        # crea nodi
        for rifugio in rifugi:
            self.G.add_node(rifugio.id, nome=rifugio.nome)


        connessioni = DAO.connessioni(year)

        # crea archi
        for connessione in connessioni:
            peso = 0
            if connessione.difficolta == 'facile':
                peso = float(connessione.distanza)
            elif connessione.difficolta == 'media':
                peso = float(connessione.distanza) * 1.5
            elif connessione.difficolta == 'difficile':
                peso = float(connessione.distanza) * 2

            self.G.add_edge(connessione.id_rifugio1, connessione.id_rifugio2, weight = peso)


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        pesi = [d["weight"] for _, _, d in self.G.edges(data=True)]
        return min(pesi), max(pesi)

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        minori = 0
        maggiori = 0
        pesi = [d["weight"] for _, _, d in self.G.edges(data=True)]
        for peso in pesi:
            if peso < soglia:
                minori+=1
            else:
                maggiori+=1
        return minori,maggiori

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO



    def cammino_minimo(self, soglia):

        Gf = nx.Graph()

        for u, v, d in self.G.edges(data=True):
            if d["weight"] > soglia:
                Gf.add_edge(u, v, weight=d["weight"])

        nodi = list(Gf.nodes())

        if len(nodi) < 3:
            return []

        best_path = None
        best_weight = float("inf")

        for i in range(len(nodi)):
            for j in range(i + 1, len(nodi)):

                start = nodi[i]
                end = nodi[j]

                try:
                    path = nx.shortest_path(Gf, source=start, target=end, weight="weight")
                except nx.NetworkXNoPath:
                    continue

                if len(path) < 3:
                    continue

                w = nx.path_weight(Gf, path, weight="weight")

                if w < best_weight:
                    best_weight = w
                    best_path = path

        if best_path is None:
            return []

        return best_path





