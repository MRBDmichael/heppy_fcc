


class Area(object):
    pass


class Circle(Area):
    
    def __init__(self, R):
        self.R = R
        self._R2 = R**2

    def is_inside(self, x_c, y_c, x, y):
        dR2 = (x - x_c)**2 + (y - y_c)**2
        return dR2 < self._R2

    
class Isolation(object):

    def __init__(self, lepton, particles, on_areas, off_areas=None,
                 pt_thresh=0, e_thresh=0):
        self.lepton = lepton
        self.particles = particles
        self.on_areas = on_areas
        if off_areas is None:
            off_areas = []
        self.off_areas = off_areas
        self.pt_thresh = pt_thresh
        self.e_thresh = e_thresh 
        self.compute()

    def compute(self):
        on_ptcs = []
        for ptc in self.particles:
            is_on = False
            for area in self.on_areas:
                if area.is_inside(self.lepton.eta(), self.lepton.phi(),
                                  ptc.eta(), ptc.phi() ):
                    is_on = True
                    break
            if not is_on:
                continue        
            for area in self.off_areas:
                if area.is_inside(self.lepton.eta(), self.lepton.phi(),
                                  ptc.eta(), ptc.phi() ):
                    is_on = False
                    break
            if is_on:
                on_ptcs.append(ptc)
        self.sumpt, self.sume, self.num = self.iso_quantities(on_ptcs)
                                
    def iso_quantities(self, ptcs):
        sumpt = 0.
        sume = 0
        num = 0
        for ptc in ptcs:
            if ptc.e()>self.e_thresh and ptc.pt()>self.pt_thresh:
                sumpt += ptc.pt()
                sume += ptc.e()
                num += 1
        return sumpt, sume, num 


        
                
