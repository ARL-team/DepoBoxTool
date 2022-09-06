from main import *

allbin = list(logspace(-4, 3, 100) * 1e-6)


#plot observations
def PLT_OBS(ax):
    researchid = df.researchid.unique()
    obs = dict()
    for id in researchid:
        obs[id] = df[df.researchid == id]

    markers = ['o','v','^','<','>','1','2','3','4','8','s','p','P','*','h','H','+','x','X','D','d','|','_']

    n = 0
    for k, v in obs.items():
        name = k
        year = v.researchyear.unique()
        dim = v.dim * 1e-6
        vd = v.Vd_cm * 1e-2 #m/s
        ax.scatter(dim, vd, color='black', s=6, marker=markers[n], label= k + str(year), zorder=10)
        n = n + 1

#plot schemes
def PLT_PR11_SID(ax, color, wstar, ls, label, buffer=False):
    lowers = []
    medians = []
    uppers = []
    wstar = wstar

    for dim in allbin:
        mods =[RUN_SID(df.density[i], \
               dim, \
               df.temp[i], \
               df.press[i], \
               df.RH[i] / 100., \
               df.ustar[i], \
               df.Lo[i], \
               luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'PR11').water(), 'PR11').PR11()[0] for i in df.index]
        lower = min(mods)
        upper = max(mods)
        median = np.median(mods)
        lowers.append(lower)
        uppers.append(upper)
        medians.append(median)
    ax.plot(allbin, medians, color=color, ls=ls, label=label)
    if buffer:
        ax.fill_between(allbin, lowers, uppers, color=color, alpha=0.2)


def PLT_VGLAI_SID(ax, color, wstar, ls, label, buffer=False):
    lowers = []
    medians = []
    uppers = []
    wstar = wstar

    for dim in allbin:
        mods =[RUN_SID(df.density[i], \
               dim, \
               df.temp[i], \
               df.press[i], \
               df.RH[i] / 100., \
               df.ustar[i], \
               df.Lo[i], \
               luc(wstar, df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'VGLAI').water(), 'VGLAI').VGLAI()[0] for i in df.index]
        lower = min(mods)
        upper = max(mods)
        median = np.median(mods)
        lowers.append(lower)
        uppers.append(upper)
        medians.append(median)

    ax.plot(allbin, medians, color=color, ls=ls, label=label)
    if buffer:
        ax.fill_between(allbin, lowers, uppers, color=color, alpha=0.2)


def PLT_Z01_SID(ax, color, label, buffer=False):
    lowers = []
    medians = []
    uppers = []

    for dim in allbin:
        mods =[RUN_SID(df.density[i], \
               dim, \
               df.temp[i], \
               df.press[i], \
               df.RH[i] / 100., \
               df.ustar[i], \
               df.Lo[i], \
               luc(df.wstar[i], df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'Z01').water(), 'Z01').Z01()[0] for i in df.index]
        lower = min(mods)
        upper = max(mods)
        median = np.median(mods)
        lowers.append(lower)
        uppers.append(upper)
        medians.append(median)
    ax.plot(allbin, medians, color=color, label=label)
    if buffer:
        ax.fill_between(allbin, lowers, uppers, color=color, alpha=0.2)


def PLT_CSU_SID(ax, color, label, buffer=False):
    lowers = []
    medians = []
    uppers = []

    for dim in allbin:
        mods =[RUN_SID(df.density[i], \
               dim, \
               df.temp[i], \
               df.press[i], \
               df.RH[i] / 100., \
               df.ustar[i], \
               df.Lo[i], \
               luc(df.wstar[i], df.LAI[i], df.ustar[i], df.Uh[i], df.z0[i], df.z[i], df.d[i], 'CSU').water(), 'CSU').CSU()[0] for i in df.index]
        lower = min(mods)
        upper = max(mods)
        median = np.median(mods)
        lowers.append(lower)
        uppers.append(upper)
        medians.append(median)
    ax.plot(allbin, medians, color=color, label=label)
    if buffer:
        ax.fill_between(allbin, lowers, uppers, color=color, alpha=0.2)

#plot
plt.close()
fig = plt.figure(figsize=(5,6))
ax = fig.add_axes([.12,.08,.82,.7])
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(1e-8, 1e-4)
ax.set_xticks([i * 1e-6 for i in [0.01, 0.1, 1, 10, 100]])
ax.set_xticklabels([0.01, 0.1, 1, 10, 100], fontsize=4)
ax.set_ylim(1e-5, 1e0) #m/s
ax.set_yticks([1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0]) #m/s
ax.set_yticklabels([i * 1e2 for i in [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0]], fontsize=4) #visually to cm/s
ax.set_ylabel('Vd(cm/s)', fontsize=7)
ax.set_xlabel('Dp(%sm) on water' % r'$\mu$', fontsize=7)

df = df_water
PLT_OBS(ax)
PLT_PR11_SID(ax, 'red', 0, '-', 'PR11(w*=0)')
PLT_PR11_SID(ax, 'red', 1, '--', 'PR11(w*=1)')
PLT_PR11_SID(ax, 'red', 2, ':', 'PR11(w*=2)')
PLT_VGLAI_SID(ax, 'purple', 0, '-', 'VGLAI(w*=0)')
PLT_VGLAI_SID(ax, 'purple', 1, '--', 'VGLAI(w*=1)')
PLT_VGLAI_SID(ax, 'purple', 2, ':', 'VGLAI(w*=2)')
PLT_Z01_SID(ax, 'gray', 'Z01')
#PLT_CSU_SID(ax, 'purple', 'CSU')

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, ncol=4, loc = 'upper center', bbox_to_anchor=(0.5, 1.25), fontsize=5, frameon=False)
fig.savefig('../figs/eval_overdp_sid_water.png', dpi=300)






