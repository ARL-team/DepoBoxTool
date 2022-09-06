#all land use parameters

class luc(object):
    def __init__(self, wstar, LAI, ustar, Uh, z0, z, d, model=''):
        self.model = model
        self.wstar = wstar
        self.ustar = ustar
        self.Uh = Uh
        self.z0 = z0
        self.z = z
        self.d = d
        self.LAI = LAI


    def grass(self):
        #combinng all grass landuse type
        if self.model in ['PR11']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z = self.z,
                               wstar = self.wstar)
            return localparams

        elif self.model in ['VGLAI']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z = self.z,
                               wstar = self.wstar,
                               LAI = self.LAI,
                               A=2.0 / 1000)
            return localparams

        #STAGE grass are using cforest parameters, will change it later
        elif self.model in ['STAGE']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z = self.z,
                               wstar = self.wstar,
                               surface = 'vegetation',
                               alpha = (1.0+0.6)/2,
                               LAI = self.LAI,
                               A = (2+5)/2/1000)
            return localparams

        elif self.model in ['Z01']:
            localparams = dict(z0 = self.z0,
                               z = self.z,
                               d = self.d,
                               surface = 'vegetation',
                               gamma = 0.54,
                               alpha = 1.2,
                               beta = 2.,
                               A = 2.0/1000)
            return localparams

        elif self.model in ['CSU']:
            localparams = dict(z0 = self.z0,
                               z = self.z,
                               d = self.d,
                               surface = 'vegetation',
                               alpha = 1.2,
                               LAI = self.LAI,
                               A = 2.0/1000)
            return localparams

        else:
            print('no model is defined')

    def cforest(self):
        #evergreen, mix needle and broadleaf
        if self.model in ['PR11']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z = self.z,
                               wstar = self.wstar)
            return localparams

        elif self.model in ['VGLAI']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z = self.z,
                               wstar = self.wstar,
                               LAI = self.LAI,
                               A=(2 + 5) / 2 / 1000)
            return localparams

        elif self.model in ['STAGE']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z = self.z,
                               wstar = self.wstar,
                               surface = 'vegetation',
                               alpha = (1.0+0.6)/2,
                               LAI = self.LAI,
                               A = (2+5)/2/1000)
            return localparams

        elif self.model in ['Z01']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z = self.z,
                               surface = 'vegetation',
                               gamma = (0.56+0.58)/2,
                               alpha = (1.0+0.6)/2,
                               beta = 2.,
                               A = (2+5)/2/1000)
            return localparams

        elif self.model in ['CSU']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z = self.z,
                               surface = 'vegetation',
                               alpha = (1.0+0.6)/2,
                               LAI = self.LAI,
                               A = (2+5)/2/1000)
            return localparams

        else:
            print('no model is defined')

    def dforest(self):
        #deciduous forest
        #because CMAQ landuse does not classify needleleaf and broadleaf, so params are taken averaged value from
        #both landuse types
        #needle + broad / 2.
        if self.model in ['PR11']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z = self.z,
                               wstar = self.wstar)
            return localparams

        elif self.model in ['VGLAI']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z = self.z,
                               wstar = self.wstar,
                               LAI = self.LAI,
                               A=3.5 / 1000)
            return localparams

        # STAGE dforest are using cforest parameters, will change it later
        elif self.model in ['STAGE']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z = self.z,
                               wstar = self.wstar,
                               surface = 'vegetation',
                               alpha = (1.0+0.6)/2,
                               LAI = self.LAI,
                               A = (2+5)/2/1000)
            return localparams

        elif self.model in ['Z01']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z =  self.z,
                               surface = 'vegetation',
                               gamma = 0.56,
                               alpha = (1.1 + .8)/2.,
                               beta = 2.,
                               A = 3.5/1000)
            return localparams

        elif self.model in ['CSU']:
            localparams = dict(z0 = self.z0,
                               d=self.d,
                               z =  self.z,
                               surface = 'vegetation',
                               alpha = (1.1 + .8)/2.,
                               LAI = self.LAI,
                               A = 3.5/1000)
            return localparams

        else:
            print('no model is defined')

    def water(self):
        #waterface, unavailable parameters will use grass as surrogate
        if self.ustar <= 0.16:
            z0 = 0.021 * self.ustar ** 3.32
        else:
            z0 = 0.00098 * self.ustar ** 1.65

        #will use above equation to calculate z0
        if self.model in ['PR11']:
            localparams = dict(z0 = z0,
                               d = self.d,
                               z = self.z,
                               wstar = self.wstar)
            return localparams

        elif self.model in ['VGLAI']:
            localparams = dict(z0 = z0,
                               d = self.d,
                               z = self.z,
                               wstar = self.wstar,
                               LAI = self.LAI,
                               A = 2.0/1000)
            return localparams

        # STAGE water are using cforest parameters, will change it later
        elif self.model == 'STAGE':
            localparams = dict(z0 = z0,
                               d=self.d,
                               z = self.z,
                               wstar = self.wstar,
                               surface = 'smooth',
                               alpha = (1.0+0.6)/2,
                               LAI = self.LAI,
                               A = (2+5)/2/1000)
            return localparams

        elif self.model == 'Z01':
            localparams = dict(z0 = z0,
                               d = self.d,
                               z = self.z,
                               surface = 'smooth',
                               gamma = 0.50,
                               alpha = 100.,
                               beta = 2.,
                               A = 2.0/1000)
            return localparams

        elif self.model == 'CSU':
            localparams = dict(z0 = z0,
                               d= self.d,
                               z = self.z,
                               surface = 'smooth',
                               alpha = 100.,
                               LAI = self.LAI,
                               A = 2.0/1000)
            return localparams

        else:
            print('no model is defined')
