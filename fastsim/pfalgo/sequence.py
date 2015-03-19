from pfinput import PFInput
from linker import Linker
from distance import distance
from floodfill import FloodFill

#TODO: this class and PFInput should probably be in the fastsim module, to try to keep the pfalgo package independent from the dataformat in use. 

class PFSequence(object):
    
    def __init__(self, simptcs):
        self.recptcs = self.reconstruct(simptcs)

    def reconstruct(self, simptcs):
        self.pfinput = PFInput(simptcs)
        elements = self.pfinput.element_list()
        self.linker = Linker(elements, distance)
        print self.pfinput
        print self.linker
        floodfill = FloodFill(elements)
        print floodfill
