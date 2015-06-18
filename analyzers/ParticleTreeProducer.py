from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy_fcc.analyzers.ntuple import *

from ROOT import TFile

class ParticleTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(ParticleTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree('particles', '')
        bookParticle(self.tree, 'ptc')
        bookParticle(self.tree, 'ptc_match')
        bookParticle(self.tree, 'ptc_match_211')
        bookParticle(self.tree, 'ptc_match_130')
        bookParticle(self.tree, 'ptc_match_22')
        
    def process(self, event):
        particles = getattr(event, self.cfg_ana.particles)
        for ptc in particles: 
            self.tree.reset()
            fillParticle(self.tree, 'ptc', ptc)
            if hasattr(ptc, 'match') and ptc.match:
                fillParticle(self.tree, 'ptc_match', ptc.match)
            if hasattr(ptc, 'match_211') and ptc.match_211:
                fillParticle(self.tree, 'ptc_match_211', ptc.match_211)
            if hasattr(ptc, 'match_130') and ptc.match_130:
                fillParticle(self.tree, 'ptc_match_130', ptc.match_130)
            if hasattr(ptc, 'match_22') and ptc.match_22:
                fillParticle(self.tree, 'ptc_match_22', ptc.match_22)
            self.tree.tree.Fill()
        
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        