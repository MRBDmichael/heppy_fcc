import random
#TODO get rid of vectors
from vectors import *
from ROOT import TLorentzVector
import math

from pfobjects import Particle

m_e = 0.000511
m_mu = 0.105
m_pi = 0.139
m_K0 = 0.498
m_n = 1.
m_p = 1. 
particle_data = {
    11 : (m_e, 1),    
    -11 : (m_e, -1),    
    13 : (m_mu, 1),    
    -13 : (m_mu, -1),    
    22 : (0., 0),
    130 : (m_K0, 0),
    211 : (m_pi, 1),
    -211 : (m_pi, -1)
    }

def particles(nptcs, pdgid, thetamin, thetamax, emin, emax, vertex=None ):
    ngenerated = 0
    mass, charge = particle_data[pdgid]
    while ngenerated<nptcs: 
        theta = random.uniform(thetamin, thetamax)
        phi = random.uniform(-math.pi, math.pi)
        energy = random.uniform(emin, emax)
        if vertex is None:
            vertex = Point(0, 0, 0)
        momentum = math.sqrt(energy**2 - mass**2)
        costheta = math.cos(theta)
        sintheta = math.sin(theta)
        cosphi = math.cos(phi)
        sinphi = math.sin(phi)        
        p4 = LorentzVector(momentum*sintheta*cosphi,
                           momentum*sintheta*sinphi,
                           momentum*costheta,
                           energy)
        ngenerated += 1
        yield Particle(p4, vertex, charge, pdgid) 

        
def monojet(pdgids, theta, pstar, jetenergy, vertex=None):
    particles = []
    if vertex is None:
        vertex = TVector3(0.,0.,0.)
    jetp4star = TLorentzVector()
    for pdgid in pdgids[:-1]:
        mass, charge = particle_data[pdgid]
        phistar = random.uniform(-math.pi, math.pi)
        thetastar = random.uniform(-math.pi, math.pi)
        sint = math.sin(thetastar)
        cost = math.cos(thetastar)
        sinp = math.sin(phistar)
        cosp = math.cos(phistar)
        pz = pstar * cost
        px = pstar * sint * cosp
        py = pstar * sint * sinp
        p4 = TLorentzVector()
        p4.SetXYZM(px, py, pz, mass)
        jetp4star += p4
        particles.append( Particle(p4, vertex, charge, pdgid) ) 
    pdgid = pdgids[-1]    
    mass, charge = particle_data[pdgid]
    p4 = TLorentzVector()
    p4.SetVectM(-jetp4star.Vect(), mass)
    particles.append( Particle(p4, vertex, charge, pdgid ))
    jetp4star += p4

    #boosting to lab
    gamma = jetenergy / jetp4star.M()
    beta = math.sqrt(1-1/gamma**2)
    boostvec = TVector3(math.sin(theta), 0, math.cos(theta))
    boostvec *= beta
    boosted_particles = []
    jetp4 = LorentzVector() 
    for ptc in particles:
        bp4 = LorentzVector(ptc.p4)
        bp4.Boost(boostvec)
        jetp4 += bp4
        boosted_particles.append( Particle(bp4,
                                           ptc.vertex,
                                           ptc.charge,
                                           ptc.pdgid) )
    print jetp4.M(), jetp4.E()
    return boosted_particles
        
if __name__ == '__main__':
    # for ptc in particles(10, 0., 0., 0.1, 0.2, 10, 50):
    #     print ptc

    for ptc in monojet([211, 22, 22], 1, 0.5, 50):
        print ptc
