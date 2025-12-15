from model.model import Model

model = Model()

model.build_weighted_graph(2000)
model.count_edges_by_threshold(4)

model.cammino_minimo_recursive()
print("ricorsione")
print(model.cammino_minimo_recursive())