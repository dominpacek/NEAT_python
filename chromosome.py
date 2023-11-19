
class Chromosome:
    def __init__(self, layers=None):
        if layers is None:
            layers = [7, 16, 16, 2]
        self.layers = layers

    def fitness(self):
        pass