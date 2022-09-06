#07/01. Added CSU and STAGE schemes into core functions for future test.
#08/01. Added composition analysis for some schemes to test EIM, EIN and EB, will add it ass a global function.
#10/03. Removed some schemes (PZ10, ZS14, ZH14), will add it later.
#10/03. Renamed CMAQ related schemes to match their names in the GMD paper.
#10/03. Unify the scheme name for single diameter, modal and bin sector methods and redefine class that needs to be
#       Called for different purposes.
#       For example, if you want to use single diameter. call RUN_SID
#       For using modal methods, call RUN_MOD
#       For using bin sectional methods, call RUN_BIN (will add it later)
#       For using diagnostic tools, call RUN_DIAG (will add it later)


from numpy import *

defaultkey = dict(
    # (values, units, physical meaning)
    # constant
    pi=(3.1416, '/', 'constant'),
    g=(9.8, 'm/s2', 'gravity accelaration'),
    kvon=(0.4, '/', 'Von Karman constant'),
    kbo=(1.38e-23, 'J/K', 'Boltzmann constant'),


    # varaibles
    dens=(1500, 'Kg/m3', 'particle density'),
    dim=(2.5e-6, 'm', 'particle diameter'),
    temp=(298, 'K', 'temperature'),
    RH=(0.9, '/', 'relative humidity'),
    press=(101325, 'Pasca', 'pressure'),
    ustar=(0.5, 'm/s', 'friction velocity'),

    # calculate using T later
    kvair=(1.57e-5, 'm2/s', 'kinematic viscosity of air, as function of Temp'),
    dvair=(1.89e-5, 'kg/m/s', 'Dynamic viscosity of air, for Vg, as function of Temp'),
    mfpath=(0.067e-6, 'm', 'air molecules mean free path'), #PZ10

    # refine in Landuse.py
    z=(0, 'm', 'measurement height'),
    Lo=(50, 'm', 'Monin-Obukhov length'),
    zr=(1, 'm', 'height at which the Vd is evaluated'),
    z0=(0.03, 'm', 'roughness length'),
    surface=([], '', 'vegetation or else')  # for different models, use different keywords
    )

class __SID(object):
    def __init__(self, dens, dim, temp, press, RH, ustar, Lo, par=dict()):
        # variables
        self.dens = dens
        self.dim = dim
        self.temp = temp
        self.press = press
        self.RH = RH
        self.ustar = ustar
        self.Lo = Lo
        self.par = par

        # constant
        self.g = 9.8
        self.kvon = 0.4
        self.kbo = 1.38e-23

        # ACP page 909, eq(19.18)
        self.dvair = 1.8e-5 * (self.temp / 298) ** 0.85
        #self.dvair2 = 1.458e-6 * (self.temp) * sqrt(self.temp) / (self.temp + 110.4)

        airdens = 1.225  # kg/m3
        self.kvair = self.dvair / airdens
        # ACP page 401, assume z= Ma/Mb = 1
        self.mfpath = self.kbo * self.temp / (sqrt(2) * pi * self.press * self.dim ** 2)
        self.C = 1 + 2 * (self.mfpath / self.dim) * (1.257 + 0.4 * exp((-0.55) * self.dim / self.mfpath))
        self.Vg = (self.dens * (self.dim) ** 2 * self.g) / (18 * self.dvair) * self.C

    def PR11(self):
        #original PR11 scheme used in CMAQ versions before v5.3
        # phiH is the stability function for heat.
        self.zr = self.par['z'] - self.par['d']

        if (1/self.Lo) < 0:
            phiH = 2 * log((sqrt(1 - 16 * self.zr / self.Lo)+1)/(sqrt(1-16*self.par['z0']/self.Lo)+1))
        elif (self.zr - self.par['z0'])/self.Lo <=1:
            phiH = -5 * (self.zr - self.par['z0']) / self.Lo
        else:
            phiH = 1 - 5 * (self.zr - self.par['z0']) / self.Lo
        Ra = 0.95 * (log(self.zr / self.par['z0']) - phiH) / (self.kvon * self.ustar)
        D = self.C * self.kbo * self.temp / (3 * pi * self.dvair * self.dim)
        Sc = self.kvair / D
        St = self.Vg * self.ustar ** 2 / (self.g * self.kvair)
        c = 400
        EIM = St ** 2 / (c + St ** 2)
        EIN = 0          # EIN is not used in CMAQ
        convfact = 1 + 0.24 * (self.par['wstar'] / self.ustar) ** 2
        EB = Sc**(-2/3.)
        Rb = 1 / (convfact * self.ustar * (EB + EIM + EIN))
        fustar = (convfact * self.ustar)
        Vd = self.Vg / (1 - exp(-self.Vg * (Ra + Rb)))
        return [Vd, self.Vg, Ra, Rb, fustar, EB, EIM, EIN]

    def VGLAI(self):
        #proposed new scheme and used for CMAQ version 5.3
        # phiH is the stability function for heat.
        self.zr = self.par['z'] - self.par['d']

        if (1/self.Lo) < 0:
            phiH = 2 * log((sqrt(1 - 16 * self.zr / self.Lo)+1)/(sqrt(1-16*self.par['z0']/self.Lo)+1))
        elif (self.zr - self.par['z0'])/self.Lo <=1:
            phiH = -5 * (self.zr - self.par['z0']) / self.Lo
        else:
            phiH = 1 - 5 * (self.zr - self.par['z0']) / self.Lo
        Ra = 0.95 * (log(self.zr / self.par['z0']) - phiH) / (self.kvon * self.ustar)
        D = self.C * self.kbo * self.temp / (3 * pi * self.dvair * self.dim)
        Sc = self.kvair / D
        St = self.Vg * self.ustar / (self.par['A'] * self.g)
        c = 1
        EIM = St ** 2 / (c + St ** 2)
        EIN = 0          # EIN is not used in CMAQ
        fveg = 1         # for single luc
        convfact = (1 + fveg * max(0,self.par['LAI']-1)) * ( 1 +  0.24 * (self.par['wstar'] / self.ustar) ** 2)
        EB = Sc**(-2/3.)
        Rb = 1 / (convfact * self.ustar * (EB + EIM + EIN))
        fustar = (convfact * self.ustar)
        Vd = self.Vg / (1 - exp(-self.Vg * (Ra + Rb)))

        #add composition analysis
        Vd_VG = self.Vg
        Rs_EB = 1 / (convfact * self.ustar * (EB))
        Vd_EB = 1 / (Ra + Rs_EB)
        Rs_EIM = 1 / (convfact * self.ustar * (EIM))
        Vd_EIM = 1 / (Ra + Rs_EIM)
        Rs_EIN = 1 / (convfact * self.ustar * (EIN))
        Vd_EIN = 1 / (Ra + Rs_EIN)
        return [Vd, Vd_VG, Vd_EB, Vd_EIM, Vd_EIN]

    def STAGE(self):
        self.zr = self.par['z'] - self.par['d']
        if (1/self.Lo) < 0:
            phiH = 2 * log((sqrt(1 - 16 * self.zr / self.Lo)+1)/(sqrt(1-16*self.par['z0']/self.Lo)+1))
        elif (self.zr - self.par['z0'])/self.Lo <=1:
            phiH = -5 * (self.zr - self.par['z0']) / self.Lo
        else:
            phiH = 1 - 5 * (self.zr - self.par['z0']) / self.Lo
        Ra = 0.95 * (log(self.zr / self.par['z0']) - phiH) / (self.kvon * self.ustar)

        D = self.C * self.kbo * self.temp / (3 * pi * self.dvair * self.dim)
        Sc = self.kvair / D

        #only test vegetation right now, will modify it later
        EB = Sc ** (-2/3)
        St = self.Vg * self.ustar / (self.g * self.par['A'])
        EIM = St ** 2 / (1 + St ** 2)
        EIN = 0

        #v_fac, get from jesse code, will define later
        v_fac = max(self.par['LAI'], 1.0)
        Rs = 1 / (v_fac * self.ustar * (EB + EIM + EIN))
        Vd = self.Vg / (1 - exp(-self.Vg * (Ra + Rs)))

        #add composition analysis
        Vd_VG = self.Vg
        Rs_EB = 1 / (v_fac * self.ustar * (EB))
        Vd_EB = 1 / (Ra + Rs_EB)
        Rs_EIM = 1 / (v_fac * self.ustar * (EIM))
        Vd_EIM = 1 / (Ra + Rs_EIM)
        return [Vd, Vd_VG, Vd_EB, Vd_EIM, Vd_EIN]

    def Z01(self):
        # phiH is the stability function for heat.
        self.zr = self.par['z'] - self.par['d']
        x = self.par['z'] / self.Lo

        if (x <= 0):
            phiH = 2 * log(0.5 * (1 + (1 - 16 * x) ** (0.5)))
        elif (x > 0):
            phiH = -5 * x
        else:
            print('Error, x is not in the range')

        Ra = (log(self.zr / self.par['z0']) - phiH) / (self.kvon * self.ustar)
        D = self.C * self.kbo * self.temp / (3 * pi * self.dvair * self.dim)
        Sc = self.kvair / D
        EB = Sc ** (-self.par['gamma'])

        if self.par['surface'] == 'smooth':
            St = self.Vg * (self.ustar) ** 2 / (self.g * self.kvair)
            EIM = 10 ** (-3 / St)
        elif self.par['surface'] == 'vegetation':
            St = self.Vg * self.ustar / (self.g * self.par['A'])
            EIM = (St / (self.par['alpha'] + St)) ** (self.par['beta'])
        else:
            print('not valid surface key word')

        EIN = 0.5 * (self.dim / self.par['A']) ** 2
        R1 = exp(-(St ** 0.5))
        e0 = 3  # empirical constant
        Rs = 1 / (e0 * self.ustar * (EB + EIM + EIN) * R1)
        fustar = (e0 * R1 * self.ustar)
        Vd = self.Vg + 1 / (Ra + Rs)

        #add composition analysis
        Vd_VG = self.Vg
        Rs_EB = 1 / (e0 * self.ustar * (EB) * R1)
        Vd_EB = 1 / (Ra + Rs_EB)
        Rs_EIM = 1 / (e0 * self.ustar * (EIM) * R1)
        Vd_EIM = 1 / (Ra + Rs_EIM)
        Rs_EIN = 1 / (e0 * self.ustar * (EIN) * R1)
        Vd_EIN = 1 / (Ra + Rs_EIN)
        return [Vd, Vd_VG, Vd_EB, Vd_EIM, Vd_EIN]

    def CSU(self):
        # phiH is the stability function for heat.
        self.zr = self.par['z'] - self.par['d']
        x = self.par['z'] / self.Lo

        if (x <= 0):
            phiH = 2 * log(0.5 * (1 + (1 - 16 * x) ** (0.5)))
        elif (x > 0):
            phiH = -5 * x
        else:
            print('Error, x is not in the range')

        Ra = (log(self.zr / self.par['z0']) - phiH) / (self.kvon * self.ustar)
        D = self.C * self.kbo * self.temp / (3 * pi * self.dvair * self.dim)
        Sc = self.kvair / D
        EB = 0.2 * Sc ** (-2/3)


        St = self.Vg * self.ustar / (self.g * self.par['A'])
        EIM = 0.4 * (St / (self.par['alpha'] + St)) ** (1.7)
        EIN = 2.5 * (self.dim / self.par['A']) ** 0.8
        R1 = exp(-(St ** 0.5))
        v_fac = max(self.par['LAI'], 1)
        Rs = 1 / (v_fac * self.ustar * (EB + EIM + EIN) * R1)
        fustar = (v_fac * R1 * self.ustar)
        Vd = self.Vg + 1 / (Ra + Rs)

        #add composition analysis
        Vd_VG = self.Vg
        Rs_EB = 1 / (v_fac * self.ustar * (EB) * R1)
        Vd_EB = 1 / (Ra + Rs_EB)
        Rs_EIM = 1 / (v_fac * self.ustar * (EIM) * R1)
        Vd_EIM = 1 / (Ra + Rs_EIM)
        Rs_EIN = 1 / (v_fac * self.ustar * (EIN) * R1)
        Vd_EIN = 1 / (Ra + Rs_EIN)
        return [Vd, Vd_VG, Vd_EB, Vd_EIM, Vd_EIN]

class __MOD(object):
    def __init__(self, dens, dim, temp, press, RH, ustar, Lo, par=dict()):
        # variables
        self.dens = dens
        self.dim = dim
        self.temp = temp
        self.press = press
        self.RH = RH
        self.ustar = ustar
        self.Lo = Lo
        self.par = par

        # constant
        self.g = 9.8
        self.kvon = 0.4
        self.kbo = 1.38e-23

        # ACP page 909, eq(19.18)
        self.dvair = 1.8e-5 * (self.temp / 298) ** 0.85
        #self.dvair2 = 1.458e-6 * (self.temp) * sqrt(self.temp) / (self.temp + 110.4)

        airdens = 1.225  # kg/m3
        self.kvair = self.dvair / airdens
        # ACP page 401, assume z= Ma/Mb = 1
        self.mfpath = self.kbo * self.temp / (sqrt(2) * pi * self.press * self.dim ** 2)
        self.C = 1 + 2 * (self.mfpath / self.dim) * (1.257 + 0.4 * exp((-0.55) * self.dim / self.mfpath))
        self.Vg = (self.dens * (self.dim) ** 2 * self.g) / (18 * self.dvair) * self.C

    #modal method is applied for all schemes that is used or proposed to be used in CMAQ.
    def PR11(self):
        # phiH is the stability function for heat.
        self.zr = self.par['z'] - self.par['d']

        if (1/self.Lo) < 0:
            phiH = 2 * log((sqrt(1 - 16 * self.zr / self.Lo)+1)/(sqrt(1-16*self.par['z0']/self.Lo)+1))
        elif (self.zr - self.par['z0'])/self.Lo <=1:
            phiH = -5 * (self.zr - self.par['z0']) / self.Lo
        else:
            phiH = 1 - 5 * (self.zr - self.par['z0']) / self.Lo

        Ra = 0.95 * (log(self.zr / self.par['z0']) - phiH) / (self.kvon * self.ustar)
        EIN = 0
        convfact = 1 + 0.24 * (self.par['wstar'] / self.ustar) ** 2
        fustar = (convfact * self.ustar)

        #mode options
        #k = 0 for number concentration, k = 2 for surface area, k = 3 for volume.
        #k = 3 is default for CMAQ as mass concentration, however, not all field measurement researches use
        #volume for collected observations, you need to switch k mannually to adpat to different measurement. k switch
        #is now added into function inputs for schemes that will apply modal methods.

        logsigmag2 = log(self.sigmag) ** 2
        k = self.moment

        if self.modeVg:
            dimg = self.dim
            Vgmean = (dimg) ** 2 * self.dens * self.g / (18 * self.dvair)
            Vghat = Vgmean *  (exp((4*k+4)/2. * logsigmag2) + 1.246 * (2*self.mfpath/dimg) * exp((2*k+1)/2. * logsigmag2))
            myVg = Vghat
        else:
            myVg = self.Vg

        if self.modeEB:
            dimg = self.dim
            Dmean = self.kbo * self.temp / (3 * pi * self.dvair * dimg)
            Dhat = Dmean * (exp((-2*k+1)/2. * logsigmag2) + 1.246 * (2*self.mfpath/dimg) * exp((-4*k+4)/2. * logsigmag2))
            myD = Dhat
            Sc = self.kvair / myD
            EB = Sc**(-2/3.)
        else:
            D = self.kbo * self.temp / (3 * pi * self.dvair * self.dim) * self.C
            Sc = self.kvair / D
            EB = Sc**(-2/3.)

        if self.modeEIM:
            Vgmean = (self.dim) ** 2 * self.dens * self.g / (18 * self.dvair)
            St = Vgmean * self.ustar ** 2 / (self.g * self.kvair)
            if k == 0:
                EIM = min(St **2 /400 * exp(8*logsigmag2), 1.0)
            elif k == 2:
                EIM = min(St **2 /400 * exp(16*logsigmag2), 1.0)
            else:
                EIM = min(St **2 /400 * exp(20*logsigmag2), 1.0)
        else:
            St = self.ustar ** 2 / (self.g * self.kvair) * self.Vg
            EIM = St ** 2 / (400 + St ** 2)

        Rb = 1 / (convfact * self.ustar * (EB + EIM + EIN))

        Vd = myVg / (1 - exp(-myVg * (Ra + Rb)))
        return [Vd, myVg, Ra, Rb, EB, EIM, EIN]

    def VGLAI(self):
        # phiH is the stability function for heat.
        self.zr = self.par['z'] - self.par['d']

        if (1/self.Lo) < 0:
            phiH = 2 * log((sqrt(1 - 16 * self.zr / self.Lo)+1)/(sqrt(1-16*self.par['z0']/self.Lo)+1))
        elif (self.zr - self.par['z0'])/self.Lo <=1:
            phiH = -5 * (self.zr - self.par['z0']) / self.Lo
        else:
            phiH = 1 - 5 * (self.zr - self.par['z0']) / self.Lo
        Ra = 0.95 * (log(self.zr / self.par['z0']) - phiH) / (self.kvon * self.ustar)
        EIN = 0
        fveg = 1 # for single luc
        convfact = (1 + fveg * max(0, self.par['LAI'] - 1)) * (1 + 0.24 * (self.par['wstar'] / self.ustar) ** 2)
        fustar = (convfact * self.ustar)

        #mode options
        logsigmag2 = log(self.sigmag) ** 2
        k = self.moment
        #k = 0 # for grass and coniferous forest because they both use number concentration
        #k = 3 # for deciduous forst because they use mass concentration

        if self.modeVg:
            dimg = self.dim
            Vgmean = (dimg) ** 2 * self.dens * self.g / (18 * self.dvair)
            Vghat = Vgmean *  (exp((4*k+4)/2. * logsigmag2) + 1.246 * (2*self.mfpath/dimg) * exp((2*k+1)/2. * logsigmag2))
            myVg = Vghat
        else:
            myVg = self.Vg


        if self.modeEB:
            dimg = self.dim
            Dmean = self.kbo * self.temp / (3 * pi * self.dvair * dimg)
            Dhat = Dmean * (exp((-2*k+1)/2. * logsigmag2) + 1.246 * (2*self.mfpath/dimg) * exp((-4*k+4)/2. * logsigmag2))
            myD = Dhat
            Sc = self.kvair / myD
            EB = Sc**(-2/3.)
        else:
            D = self.C * self.kbo * self.temp / (3 * pi * self.dvair * self.dim)
            Sc = self.kvair / D
            EB = Sc**(-2/3.)

        if self.modeEIM:
            print('VGLAI does not use modeEIM')
        else:
            pass

        St = myVg * self.ustar / (self.g * self.par['A'])
        EIM = St ** 2 / (1 + St **2)
        Rb = 1 / (convfact * self.ustar * (EB + EIM + EIN))
        Vd = myVg / (1 - exp(-myVg * (Ra + Rb)))
        return [Vd, myVg, Ra, Rb, EB, EIM, EIN]


class __DIAG(object):
    def __init__(self, dens, dim, temp, press, RH, ustar, Lo, par=dict()):
        # variables
        self.dens = dens
        self.dim = dim
        self.temp = temp
        self.press = press
        self.RH = RH
        self.ustar = ustar
        self.Lo = Lo
        self.par = par

        # constant
        self.g = 9.8
        self.kvon = 0.4
        self.kbo = 1.38e-23

        # ACP page 909, eq(19.18)
        self.dvair = 1.8e-5 * (self.temp / 298) ** 0.85
        #self.dvair2 = 1.458e-6 * (self.temp) * sqrt(self.temp) / (self.temp + 110.4)

        airdens = 1.225  # kg/m3
        self.kvair = self.dvair / airdens
        # ACP page 401, assume z= Ma/Mb = 1
        self.mfpath = self.kbo * self.temp / (sqrt(2) * pi * self.press * self.dim ** 2)
        self.C = 1 + 2 * (self.mfpath / self.dim) * (1.257 + 0.4 * exp((-0.55) * self.dim / self.mfpath))
        self.Vg = (self.dens * (self.dim) ** 2 * self.g) / (18 * self.dvair) * self.C

    #modal method is applied for all schemes that is used or proposed to be used in CMAQ.
    def PR11(self):
        # phiH is the stability function for heat.
        self.zr = self.par['z'] - self.par['d']

        if (1/self.Lo) < 0:
            phiH = 2 * log((sqrt(1 - 16 * self.zr / self.Lo)+1)/(sqrt(1-16*self.par['z0']/self.Lo)+1))
        elif (self.zr - self.par['z0'])/self.Lo <=1:
            phiH = -5 * (self.zr - self.par['z0']) / self.Lo
        else:
            phiH = 1 - 5 * (self.zr - self.par['z0']) / self.Lo

        Ra = 0.95 * (log(self.zr / self.par['z0']) - phiH) / (self.kvon * self.ustar)
        EIN = 0
        convfact = 1 + 0.24 * (self.par['wstar'] / self.ustar) ** 2
        fustar = (convfact * self.ustar)

        #mode options
        #k = 0 for number concentration, k = 2 for surface area, k = 3 for volume.
        #k = 3 is default for CMAQ as mass concentration, however, not all field measurement researches use
        #volume for collected observations, you need to switch k mannually to adpat to different measurement. k switch
        #is now added into function inputs for schemes that will apply modal methods.

        logsigmag2 = log(self.sigmag) ** 2
        k = self.moment

        if self.modeVg:
            dimg = self.dim
            Vgmean = (dimg) ** 2 * self.dens * self.g / (18 * self.dvair)
            Vghat = Vgmean *  (exp((4*k+4)/2. * logsigmag2) + 1.246 * (2*self.mfpath/dimg) * exp((2*k+1)/2. * logsigmag2))
            myVg = Vghat
        else:
            myVg = self.Vg

        if self.modeEB:
            dimg = self.dim
            Dmean = self.kbo * self.temp / (3 * pi * self.dvair * dimg)
            Dhat = Dmean * (exp((-2*k+1)/2. * logsigmag2) + 1.246 * (2*self.mfpath/dimg) * exp((-4*k+4)/2. * logsigmag2))
            myD = Dhat
            Sc = self.kvair / myD
            EB = Sc**(-2/3.)
        else:
            D = self.kbo * self.temp / (3 * pi * self.dvair * self.dim) * self.C
            Sc = self.kvair / D
            EB = Sc**(-2/3.)

        if self.modeEIM:
            Vgmean = (self.dim) ** 2 * self.dens * self.g / (18 * self.dvair)
            St = Vgmean * self.ustar ** 2 / (self.g * self.kvair)
            if k == 0:
                EIM = min(St **2 /400 * exp(8*logsigmag2), 1.0)
            elif k == 2:
                EIM = min(St **2 /400 * exp(16*logsigmag2), 1.0)
            else:
                EIM = min(St **2 /400 * exp(20*logsigmag2), 1.0)
        else:
            St = self.ustar ** 2 / (self.g * self.kvair) * self.Vg
            EIM = St ** 2 / (400 + St ** 2)

        Rb = 1 / (convfact * self.ustar * (EB + EIM + EIN))

        Vd = myVg / (1 - exp(-myVg * (Ra + Rb)))
        return [Vd, myVg, myVg/Vd]


class RUN_SID(__SID):
    def __init__(self, dens, dim, temp, press, RH, ustar, Lo, par, model=''):
        """
        model options: PR11 VGLAI STAGE Z01 STAGE
        more models can be added later
        """
        super().__init__(dens=dens, dim=dim, temp=temp, press=press, RH=RH, ustar=ustar, Lo=Lo, par=par)
        self.model = model
        if model == 'Z01':
            Vd = self.Z01()[0]
            Vd_VG = self.Z01()[1]
            Vd_EB = self.Z01()[2]
            Vd_EIM = self.Z01()[3]
            Vd_EIN = self.Z01()[4]

        elif model == 'CSU':
            Vd = self.CSU()[0]
            Vg_VG = self.CSU()[1]
            Vd_EB = self.CSU()[2]
            Vd_EIM = self.CSU()[3]
            Vd_EIN = self.CSU()[4]

        elif model == 'VGLAI':
            Vd = self.VGLAI()[0]
            Vd_VG = self.VGLAI()[1]
            Vd_EB = self.VGLAI()[2]
            Vd_EIM = self.VGLAI()[3]
            Vd_EIN = self.VGLAI()[4]

        elif model == 'STAGE':
            Vd = self.STAGE()[0]
            Vd_VG = self.STAGE()[1]
            Vd_EB = self.STAGE()[2]
            Vd_EIM = self.STAGE()[3]
            Vd_EIN = self.STAGE()[4]

        elif model == 'PR11':
            Vd = self.PR11()[0]
            Vg = self.PR11()[1]

        else:
            print('No model option has been selected')


class RUN_MOD(__MOD):
    """
    model options: PR11 VGLAI
    more models can be added later
    """
    def __init__(self, dens, dim, temp, press, RH, ustar, Lo, par, sigmag, moment, model='', modeVg=False, modeEB=False, modeEIM=False):
        super().__init__(dens=dens, dim=dim, temp=temp, press=press, RH=RH, ustar=ustar, Lo=Lo, par=par)
        self.model = model
        self.sigmag = sigmag
        self.moment = moment
        self.modeVg = modeVg
        self.modeEB = modeEB
        self.modeEIM = modeEIM

class RUN_DIAG(__DIAG):
    """
    model options: PR11 VGLAI
    more models can be added later
    """
    def __init__(self, dens, dim, temp, press, RH, ustar, Lo, par, sigmag, moment, model='', modeVg=False, modeEB=False, modeEIM=False):
        super().__init__(dens=dens, dim=dim, temp=temp, press=press, RH=RH, ustar=ustar, Lo=Lo, par=par)
        self.model = model
        self.sigmag = sigmag
        self.moment = moment
        self.modeVg = modeVg
        self.modeEB = modeEB
        self.modeEIM = modeEIM

class RUN_BIN(__SID):
    """
    Under development
    """
    def __init__(self, dens, dim, temp, press, RH, ustar, Lo, par, sigmag, model=''):
        super().__init__(dens=dens, dim=dim, temp=temp, press=press, RH=RH, ustar=ustar, Lo=Lo, par=par)
        self.sigmag = sigmag




