import random
import numpy as np


class Distribution:
    def __init__(self):
        return
    

class Uniform:
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b
    
    def draw(self):
        return self.a + random.random() * (self.b-self.a)


class Gaussian:
    def __init__(self, mean, sd):
        super().__init__()
        self.mean= mean
        self.sd = mean
    
    def draw(self):
        while True:
            t = np.random.normal(self.mean, self.sd)
            if t > 0:
                return t
