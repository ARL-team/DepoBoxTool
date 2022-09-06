from main import *

allbin = list(logspace(-4, 3, 100) * 1e-6)


#plot observations
def PLT_OBS(ax, df):
    df = df
    researchid = df.researchid.unique()
    obs = dict()
    for id in researchid:
        obs[id] = df[df.researchid == id]

    for k, v in obs.items():
        dim = v.dim * 1e-6
        vd = v.Vd_cm * 1e-2
        ax.scatter(dim, vd, color='black', s=3, marker='o', label= 'obs')

#plot schemes
def PLT_MOD(ax, df, color, wstar, sigmag, moment, ls, label, lucs='', schemes='', buffer=False):
    lowers = []
    medians = []
    uppers = []
    wstar = wstar
    df = df

    for index, dim in enumerate(allbin):
        print(index, dim)

        if lucs == 'grass':
            if schemes == 'PR11':
                mods = [RUN_MOD(df.density[i], \
                                dim, \
                                df.temp[i], \
                                df.press[i], \
                                df.RH[i] / 100., \
                                df.ustar[i], \
                                df.Lo[i], \
                                luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i],'PR11').grass(), sigmag, moment, 'PR11', True, True, True).PR11()[0] for i in df.index]
            elif schemes == 'OFF':
                mods = [RUN_MOD(df.density[i], \
                                dim, \
                                df.temp[i], \
                                df.press[i], \
                                df.RH[i] / 100., \
                                df.ustar[i], \
                                df.Lo[i], \
                                luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i],'PR11').grass(), sigmag, moment, 'PR11', True, True, False).PR11()[0] for i in df.index]
            elif schemes == 'VGLAI':
                mods = [RUN_MOD(df.density[i], \
                                dim, \
                                df.temp[i], \
                                df.press[i], \
                                df.RH[i] / 100., \
                                df.ustar[i], \
                                df.Lo[i], \
                                luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i],'VGLAI').grass(), sigmag, moment, 'VGLAI', True, True, False).VGLAI()[0] for i in df.index]
            else:
                print('no scheme is selected')

        elif lucs == 'cf':
            if schemes == 'PR11':
                mods = [RUN_MOD(df.density[i], \
                                dim, \
                                df.temp[i], \
                                df.press[i], \
                                df.RH[i] / 100., \
                                df.ustar[i], \
                                df.Lo[i], \
                                luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i],'PR11').cforest(), sigmag, moment, 'PR11', True, True, True).PR11()[0] for i in df.index]
            elif schemes == 'OFF':
                mods = [RUN_MOD(df.density[i], \
                                dim, \
                                df.temp[i], \
                                df.press[i], \
                                df.RH[i] / 100., \
                                df.ustar[i], \
                                df.Lo[i], \
                                luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i],'PR11').cforest(), sigmag, moment, 'PR11', True, True, False).PR11()[0] for i in df.index]
            elif schemes == 'VGLAI':
                mods = [RUN_MOD(df.density[i], \
                                dim, \
                                df.temp[i], \
                                df.press[i], \
                                df.RH[i] / 100., \
                                df.ustar[i], \
                                df.Lo[i], \
                                luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i],'VGLAI').cforest(), sigmag, moment, 'VGLAI', True, True, False).VGLAI()[0] for i in df.index]
            else:
                print('no scheme is selected')

        elif lucs == 'df':
            if schemes == 'PR11':
                mods = [RUN_MOD(df.density[i], \
                                dim, \
                                df.temp[i], \
                                df.press[i], \
                                df.RH[i] / 100., \
                                df.ustar[i], \
                                df.Lo[i], \
                                luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i],'PR11').dforest(), sigmag, moment, 'PR11', True, True, True).PR11()[0] for i in df.index]
            elif schemes == 'OFF':
                mods = [RUN_MOD(df.density[i], \
                                dim, \
                                df.temp[i], \
                                df.press[i], \
                                df.RH[i] / 100., \
                                df.ustar[i], \
                                df.Lo[i], \
                                luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i],'PR11').dforest(), sigmag, moment, 'PR11', True, True, False).PR11()[0] for i in df.index]
            elif schemes == 'VGLAI':
                mods = [RUN_MOD(df.density[i], \
                                dim, \
                                df.temp[i], \
                                df.press[i], \
                                df.RH[i] / 100., \
                                df.ustar[i], \
                                df.Lo[i], \
                                luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i],'VGLAI').dforest(), sigmag, moment, 'VGLAI', True, True, False).VGLAI()[0] for i in df.index]
            else:
                print('no scheme is selected')

        elif lucs == 'water':
            if schemes == 'PR11':
                mods = [RUN_MOD(df.density[i], \
                                dim, \
                                df.temp[i], \
                                df.press[i], \
                                df.RH[i] / 100., \
                                df.ustar[i], \
                                df.Lo[i], \
                                luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i],'PR11').water(), sigmag, moment, 'PR11', True, True, True).PR11()[0] for i in df.index]
            elif schemes == 'OFF':
                mods = [RUN_MOD(df.density[i], \
                                dim, \
                                df.temp[i], \
                                df.press[i], \
                                df.RH[i] / 100., \
                                df.ustar[i], \
                                df.Lo[i], \
                                luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i],'PR11').water(), sigmag, moment, 'PR11', True, True, False).PR11()[0] for i in df.index]
            elif schemes == 'VGLAI':
                mods = [RUN_MOD(df.density[i], \
                                dim, \
                                df.temp[i], \
                                df.press[i], \
                                df.RH[i] / 100., \
                                df.ustar[i], \
                                df.Lo[i], \
                                luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i],'VGLAI').water(), sigmag, moment, 'VGLAI', True, True, False).VGLAI()[0] for i in df.index]
            else:
                print('no scheme is selected')

        else:
            print('no luc is selected')

        lower = min(mods)
        upper = max(mods)
        median = np.median(mods)
        lowers.append(lower)
        uppers.append(upper)
        medians.append(median)

    ax.plot(allbin, medians, color=color, ls=ls, label=label)
    if buffer:
        ax.fill_between(allbin, lowers, uppers, color=color, alpha=0.2)



#plot
fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(9,11), gridspec_kw={'wspace':0.2, 'hspace':0.15, 'left':0.1, 'right':0.95, 'bottom':0.05, 'top':0.9})
for ax in axes.flat:
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e-8, 1e-4)
    ax.set_xticks([i * 1e-6 for i in [0.01, 0.1, 1, 10, 100]])
    ax.set_xticklabels([0.01, 0.1, 1, 10, 100], fontsize=6)
    ax.set_ylim(1e-5, 1e0) #m/s
    ax.set_yticks([1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0]) #m/s
    ax.set_yticklabels([i * 1e2 for i in [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0]], fontsize=4) #visually to cm/s

axes[0,0].set_title('%sg=1.01' % r'$\sigma$', fontsize=12)
axes[0,1].set_title('%sg=1.7' % r'$\sigma$', fontsize=12)
axes[0,2].set_title('%sg=2.5' % r'$\sigma$', fontsize=12)
axes[0,0].set_ylabel('Grass Vd (cm/s)', fontsize=12)
axes[1,0].set_ylabel('Coniferous Forest', fontsize=12)
axes[2,0].set_ylabel('Deciduous Forest', fontsize=12)
axes[3,0].set_ylabel('Water', fontsize=12)
axes[3,1].set_xlabel('Dp(%sm)' % r'$\mu$', fontsize=12)

for df in [df_grass]:
    PLT_OBS(axes[0,0], df)
    PLT_OBS(axes[0,1], df)
    PLT_OBS(axes[0,2], df)

    for sigmag in [1.01]:
        PLT_MOD(axes[0,0], df, 'red', 1, sigmag, 0, '--', 'PR11', 'grass', 'PR11', False)
        PLT_MOD(axes[0,0], df, 'blue', 1, sigmag, 0,':', 'OFF', 'grass', 'OFF', False)
        PLT_MOD(axes[0,0], df, 'purple', 1, sigmag, 0, '--', 'VGLAI', 'grass', 'VGLAI', False)

    for sigmag in [1.7]:
        PLT_MOD(axes[0,1], df, 'red', 1, sigmag, 0, '--', 'PR11', 'grass', 'PR11', False)
        PLT_MOD(axes[0,1], df, 'blue', 1, sigmag, 0,':', 'OFF', 'grass', 'OFF', False)
        PLT_MOD(axes[0,1], df, 'purple', 1, sigmag, 0, '--', 'VGLAI', 'grass', 'VGLAI', False)

    for sigmag in [2.5]:
        PLT_MOD(axes[0,2], df, 'red', 1, sigmag, 0, '--', 'PR11', 'grass', 'PR11', False)
        PLT_MOD(axes[0,2], df, 'blue', 1, sigmag, 0,':', 'OFF', 'grass', 'OFF', False)
        PLT_MOD(axes[0,2], df, 'purple', 1, sigmag, 0, '--', 'VGLAI', 'grass', 'VGLAI', False)

for df in [df_cf]:
    PLT_OBS(axes[1,0], df)
    PLT_OBS(axes[1,1], df)
    PLT_OBS(axes[1,2], df)

    for sigmag in [1.01]:
        PLT_MOD(axes[1,0], df, 'red', 1, sigmag, 0, '--', 'PR11', 'cf', 'PR11', False)
        PLT_MOD(axes[1,0], df, 'blue', 1, sigmag, 0,':', 'OFF', 'cf', 'OFF', False)
        PLT_MOD(axes[1,0], df, 'purple', 1, sigmag, 0, '--', 'VGLAI', 'cf', 'VGLAI', False)

    for sigmag in [1.7]:
        PLT_MOD(axes[1,1], df, 'red', 1, sigmag, 0, '--', 'PR11', 'cf', 'PR11', False)
        PLT_MOD(axes[1,1], df, 'blue', 1, sigmag, 0,':', 'OFF', 'cf', 'OFF', False)
        PLT_MOD(axes[1,1], df, 'purple', 1, sigmag, 0, '--', 'VGLAI', 'cf', 'VGLAI', False)

    for sigmag in [2.5]:
        PLT_MOD(axes[1,2], df, 'red', 1, sigmag, 0, '--', 'PR11', 'cf', 'PR11', False)
        PLT_MOD(axes[1,2], df, 'blue', 1, sigmag, 0,':', 'OFF', 'cf', 'OFF', False)
        PLT_MOD(axes[1,2], df, 'purple', 1, sigmag, 0, '--', 'VGLAI', 'cf', 'VGLAI', False)

for df in [df_df]:
    PLT_OBS(axes[2,0], df)
    PLT_OBS(axes[2,1], df)
    PLT_OBS(axes[2,2], df)

    for sigmag in [1.01]:
        PLT_MOD(axes[2,0], df, 'red', 1, sigmag, 0, '--', 'PR11', 'df', 'PR11', False)
        PLT_MOD(axes[2,0], df, 'blue', 1, sigmag, 0,':', 'OFF', 'df', 'OFF', False)
        PLT_MOD(axes[2,0], df, 'purple', 1, sigmag, 0, '--', 'VGLAI', 'df', 'VGLAI', False)

    for sigmag in [1.7]:
        PLT_MOD(axes[2,1], df, 'red', 1, sigmag, 0, '--', 'PR11', 'df', 'PR11', False)
        PLT_MOD(axes[2,1], df, 'blue', 1, sigmag, 0,':', 'OFF', 'df', 'OFF', False)
        PLT_MOD(axes[2,1], df, 'purple', 1, sigmag, 0, '--', 'VGLAI', 'df', 'VGLAI', False)

    for sigmag in [2.5]:
        PLT_MOD(axes[2,2], df, 'red', 1, sigmag, 0, '--', 'PR11', 'df', 'PR11', False)
        PLT_MOD(axes[2,2], df, 'blue', 1, sigmag, 0,':', 'OFF', 'df', 'OFF', False)
        PLT_MOD(axes[2,2], df, 'purple', 1, sigmag, 0, '--', 'VGLAI', 'df', 'VGLAI', False)

for df in [df_water]:
    PLT_OBS(axes[3,0], df)
    PLT_OBS(axes[3,1], df)
    PLT_OBS(axes[3,2], df)

    for sigmag in [1.01]:
        PLT_MOD(axes[3,0], df, 'red', 1, sigmag, 0, '--', 'PR11', 'water', 'PR11', False)
        PLT_MOD(axes[3,0], df, 'blue', 1, sigmag, 0,':', 'OFF', 'water', 'OFF', False)
        PLT_MOD(axes[3,0], df, 'purple', 1, sigmag, 0, '--', 'VGLAI', 'water', 'VGLAI', False)

    for sigmag in [1.7]:
        PLT_MOD(axes[3,1], df, 'red', 1, sigmag, 0, '--', 'PR11', 'water', 'PR11', False)
        PLT_MOD(axes[3,1], df, 'blue', 1, sigmag, 0,':', 'OFF', 'water', 'OFF', False)
        PLT_MOD(axes[3,1], df, 'purple', 1, sigmag, 0, '--', 'VGLAI', 'water', 'VGLAI', False)

    for sigmag in [2.5]:
        PLT_MOD(axes[3,2], df, 'red', 1, sigmag, 0, '--', 'PR11', 'water', 'PR11', False)
        PLT_MOD(axes[3,2], df, 'blue', 1, sigmag, 0,':', 'OFF', 'water', 'OFF', False)
        PLT_MOD(axes[3,2], df, 'purple', 1, sigmag, 0, '--', 'VGLAI', 'water', 'VGLAI', False)

from matplotlib.lines import Line2D
patches = dict()
patches['PR11'] = Line2D([0], [0], color='red', lw=1, ls='--', label='PR11')
patches['OFF'] = Line2D([0], [0], color='blue', lw=1, ls=':', label='OFF')
patches['VGLAI'] = Line2D([0], [0], color='purple', lw=1, ls='--', label='VGLAI')
patches['OBS'] = plt.scatter([0], [0], color='black', marker='o', label='OBS')
lpatch = [v for k, v in patches.items()]
llabels = [lp.get_label() for lp in lpatch]
axes[0,1].legend(lpatch, llabels, ncol=4, loc = 'upper center', bbox_to_anchor=(0.5, 1.4), fontsize=10, frameon=False)
fig.savefig('../figs/vdoverdp_multipanels.png', dpi=300)






