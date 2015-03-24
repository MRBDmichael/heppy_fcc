from heppy_fcc.fastsim.pdt import particle_data
from heppy_fcc.fastsim.path import StraightLine, Helix
from heppy_fcc.fastsim.pfobjects import Particle

from ROOT import TVector3, TLorentzVector
import math

class PFReconstructor(object):

    def __init__(self, groups):
        self.particles = self.reconstruct(groups)

    def reconstruct(self, groups):
        particles = []
        for groupid, elemlist in groups.iteritems():
            if len(elemlist)==1:
                elem = elemlist[0]
                layer = elem.layer
                if layer == 'ecal_in' or layer == 'hcal_in':
                    particles.append(self.reconstruct_cluster(elem, layer))
                elif layer == 'tracker':
                    particles.append(self.reconstruct_track(elem))
        return particles

    def reconstruct_cluster(self, cluster, layer, vertex=None):
        if vertex is None:
            vertex = TVector3()
        pdg_id = None
        if layer=='ecal_in':
            pdg_id = 22
        elif layer=='hcal_in':
            pdg_id = 130
        else:
            raise ValueError('layer must be equal to ecal_in or hcal_in')
        assert(pdg_id)
        mass, charge = particle_data[pdg_id]
        energy = cluster.energy
        momentum = math.sqrt(energy**2 - mass**2) 
        p3 = cluster.position.Unit() * momentum
        p4 = TLorentzVector(p3.Px(), p3.Py(), p3.Pz(), energy)
        particle = Particle(p4, vertex, charge, pdg_id)
        path = StraightLine(p4, vertex)
        path.points[layer] = cluster.position
        particle.set_path(path)
        particle.clusters_smeared[layer] = cluster
        return particle
        
    def reconstruct_track(self, track):
        return None

    def __str__(self):
        return '\n'.join( map(str, self.particles) ) 