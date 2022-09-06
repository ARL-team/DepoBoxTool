from main import *
from DepoBoxTool.func_evals import MB, NMB, FB, FE, R2, RMSE

def matches(wstar, sigmag, moment, lucs='', schemes=''):
    if lucs == 'grass':
        df = df_grass
        obs_cm = np.array([df.Vd_cm[i]  for i in df.index])
        obs_m = obs_cm * 1e-2

        if schemes == 'PR11':
            mods = [RUN_MOD(df.density[i], \
                            df.dim[i] * 1e-6, \
                            df.temp[i], \
                            df.press[i], \
                            df.RH[i] / 100., \
                            df.ustar[i], \
                            df.Lo[i], \
                            luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'PR11').grass(),sigmag, moment, 'PR11', True, True, True).PR11()[0] for i in df.index]

        elif schemes == 'OFF':
            mods = [RUN_MOD(df.density[i], \
                            df.dim[i] * 1e-6, \
                            df.temp[i], \
                            df.press[i], \
                            df.RH[i] / 100., \
                            df.ustar[i], \
                            df.Lo[i], \
                            luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'PR11').grass(),sigmag, moment, 'PR11', True, True, False).PR11()[0] for i in df.index]

        elif schemes == 'VGLAI':
            mods = [RUN_MOD(df.density[i], \
                            df.dim[i] * 1e-6, \
                            df.temp[i], \
                            df.press[i], \
                            df.RH[i] / 100., \
                            df.ustar[i], \
                            df.Lo[i], \
                            luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'VGLAI').grass(),sigmag, moment, 'VGLAI', True, True, False).VGLAI()[0] for i in df.index]
        else:
            print('scheme is not included')

        return obs_m, mods

    elif lucs == 'cf':
        df = df_cf
        obs_cm = np.array([df.Vd_cm[i] for i in df.index])
        obs_m = obs_cm * 1e-2

        if schemes == 'PR11':
            mods = [RUN_MOD(df.density[i], \
                            df.dim[i] * 1e-6, \
                            df.temp[i], \
                            df.press[i], \
                            df.RH[i] / 100., \
                            df.ustar[i], \
                            df.Lo[i], \
                            luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'PR11').cforest(),sigmag, moment, 'PR11', True, True, True).PR11()[0] for i in df.index]

        elif schemes == 'OFF':
            mods = [RUN_MOD(df.density[i], \
                            df.dim[i] * 1e-6, \
                            df.temp[i], \
                            df.press[i], \
                            df.RH[i] / 100., \
                            df.ustar[i], \
                            df.Lo[i], \
                            luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'PR11').cforest(),sigmag, moment, 'PR11', True, True, False).PR11()[0] for i in df.index]

        elif schemes == 'VGLAI':
            mods = [RUN_MOD(df.density[i], \
                            df.dim[i] * 1e-6, \
                            df.temp[i], \
                            df.press[i], \
                            df.RH[i] / 100., \
                            df.ustar[i], \
                            df.Lo[i], \
                            luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'VGLAI').cforest(),sigmag, moment, 'VGLAI', True, True, False).VGLAI()[0] for i in df.index]
        else:
            print('scheme is not included')

        return obs_m, mods

    elif lucs == 'df':
        df = df_df
        obs_cm = np.array([df.Vd_cm[i] for i in df.index])
        obs_m = obs_cm * 1e-2

        if schemes == 'PR11':
            mods = [RUN_MOD(df.density[i], \
                            df.dim[i] * 1e-6, \
                            df.temp[i], \
                            df.press[i], \
                            df.RH[i] / 100., \
                            df.ustar[i], \
                            df.Lo[i], \
                            luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'PR11').dforest(),sigmag, moment, 'PR11', True, True, True).PR11()[0] for i in df.index]

        elif schemes == 'OFF':
            mods = [RUN_MOD(df.density[i], \
                            df.dim[i] * 1e-6, \
                            df.temp[i], \
                            df.press[i], \
                            df.RH[i] / 100., \
                            df.ustar[i], \
                            df.Lo[i], \
                            luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'PR11').dforest(),sigmag, moment, 'PR11', True, True, False).PR11()[0] for i in df.index]

        elif schemes == 'VGLAI':
            mods = [RUN_MOD(df.density[i], \
                            df.dim[i] * 1e-6, \
                            df.temp[i], \
                            df.press[i], \
                            df.RH[i] / 100., \
                            df.ustar[i], \
                            df.Lo[i], \
                            luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'VGLAI').dforest(),sigmag, moment, 'VGLAI', True, True, False).VGLAI()[0] for i in df.index]
        else:
            print('scheme is not included')

        return obs_m, mods


    elif lucs == 'water':
        df = df_water
        obs_cm = np.array([df.Vd_cm[i] for i in df.index])
        obs_m = obs_cm * 1e-2

        if schemes == 'PR11':
            mods = [RUN_MOD(df.density[i], \
                            df.dim[i] * 1e-6, \
                            df.temp[i], \
                            df.press[i], \
                            df.RH[i] / 100., \
                            df.ustar[i], \
                            df.Lo[i], \
                            luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'PR11').water(),sigmag, moment, 'PR11', True, True, True).PR11()[0] for i in df.index]

        elif schemes == 'OFF':
            mods = [RUN_MOD(df.density[i], \
                            df.dim[i] * 1e-6, \
                            df.temp[i], \
                            df.press[i], \
                            df.RH[i] / 100., \
                            df.ustar[i], \
                            df.Lo[i], \
                            luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'PR11').water(),sigmag, moment, 'PR11', True, True, False).PR11()[0] for i in df.index]

        elif schemes == 'VGLAI':
            mods = [RUN_MOD(df.density[i], \
                            df.dim[i] * 1e-6, \
                            df.temp[i], \
                            df.press[i], \
                            df.RH[i] / 100., \
                            df.ustar[i], \
                            df.Lo[i], \
                            luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'VGLAI').water(),sigmag, moment, 'VGLAI', True, True, False).VGLAI()[0] for i in df.index]
        else:
            print('scheme is not included')

        return obs_m, mods

    else:
        print('luc is not included')


def metrics(sigmag, lucs=''):
    print('sigmag =',sigmag, 'for', lucs)
    metrics = dict()
    for scheme in ['PR11', 'OFF','VGLAI']:
        metrics[scheme] = dict()
        #for mass, use moment=2
        obs, mod = matches(1, sigmag, 2, lucs, scheme)

        metrics[scheme]['MB'] = '%.3f' % MB(obs, mod)
        metrics[scheme]['NMB'] = '%.3f' % NMB(obs, mod)
        metrics[scheme]['FB'] = '%.3f' % FB(obs, mod)
        metrics[scheme]['FE'] = '%.3f' % FE(obs, mod)
        metrics[scheme]['R2'] = '%.3f' % R2(obs, mod)
      
    for k, v in metrics.items():
        print(k, v)

    return metrics

def main():
    metrics(1.01, 'grass')
    metrics(1.7, 'grass')
    metrics(2.5, 'grass')

    metrics(1.01, 'cf')
    metrics(1.7, 'cf')
    metrics(2.5, 'cf')

    metrics(1.01, 'df')
    metrics(1.7, 'df')
    metrics(2.5, 'df')

    metrics(1.01, 'water')
    metrics(1.7, 'water')
    metrics(2.5, 'water')

if __name__ == '__main__':
    main()














