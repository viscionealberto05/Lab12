from model.model import Model

model = Model()

model.build_weighted_graph(2020)
print(model.lista_nodi)
min, max = model.get_edges_weight_min_max()
print(min, max)