#add functions for all possible evaluation metrics
import numpy as np

def STDO(obs, mod, axis=None):
    """ Standard deviation of Observations """
    return np.ma.std(obs, axis=axis)


def STDP(obs, mod, axis=None):
    """ Standard deviation of Predictions """
    return np.ma.std(mod, axis=axis)


def MNB(obs, mod, axis=None):
    """ Mean Normalized Bias (%)"""
    return np.ma.masked_invalid((mod - obs) / obs).mean(axis=axis) * 100.


def MNE(obs, mod, axis=None):
    """ Mean Normalized Gross Error (%)"""
    ne = np.ma.abs(mod - obs) / obs
    return np.ma.masked_invalid(ne).mean(axis=axis) * 100.


def MdnNB(obs, mod, axis=None):
    """ Median Normalized Bias (%)"""
    nb = (mod - obs) / obs
    return np.ma.median(np.ma.masked_invalid(nb), axis=axis) * 100.


def MdnNE(obs, mod, axis=None):
    """ Median Normalized Gross Error (%)"""
    ne = np.ma.abs(mod - obs) / obs
    return np.ma.median(np.ma.masked_invalid(ne), axis=axis) * 100.


def NO(obs, mod, axis=None):
    """ N Observations (#)"""
    return (~np.ma.getmaskarray(obs)).sum(axis=axis)


def NOP(obs, mod, axis=None):
    """ N Observations/Prediction Pairs (#)"""
    obsc, modc = matchmasks(obs, mod)
    return (~np.ma.getmaskarray(obsc)).sum(axis=axis)


def NP(obs, mod, axis=None):
    """ N Predictions (#)"""
    return (~np.ma.getmaskarray(mod)).sum(axis=axis)


def MO(obs, mod, axis=None):
    """ Mean Observations (obs unit)"""
    return obs.mean(axis=axis)


def MP(obs, mod, axis=None):
    """ Mean Predictions (model unit)"""
    return mod.mean(axis=axis)


def MdnO(obs, mod, axis=None):
    """ Median Observations (obs unit)"""
    return np.ma.median(obs, axis=axis)


def MdnP(obs, mod, axis=None):
    """ Median Predictions (model unit)"""
    return np.ma.median(mod, axis=axis)


def RM(obs, mod, axis=None):
    """ Mean Ratio Observations/Predictions (none)"""
    return np.ma.masked_invalid(obs / mod).mean(axis=axis)


def RMdn(obs, mod, axis=None):
    """ Median Ratio Observations/Predictions (none)"""
    return np.ma.median(np.ma.masked_invalid(obs / mod), axis=axis)


def MB(obs, mod, axis=None):
    """ Mean Bias"""
    return (mod - obs).mean(axis=axis)


def MdnB(obs, mod, axis=None):
    """ Median Bias"""
    return np.ma.median(mod - obs, axis=axis)


def NMB(obs, mod, axis=None):
    """ Normalized Mean Bias (%)"""
    return (mod - obs).sum(axis=axis) / obs.sum(axis=axis) * 100.


def NMdnB(obs, mod, axis=None):
    """ Normalized Median Bias (%)"""
    mdnb = np.ma.median(mod - obs, axis=axis)
    mdno = np.ma.median(obs, axis=axis)
    return mdnb / mdno * 100.


def FB(obs, mod, axis=None):
    """ Fractional Bias (%)"""
    halffb = (mod - obs) / (mod + obs)
    return ((np.ma.masked_invalid(halffb)).mean(axis=axis) * 2.) * 100.


def ME(obs, mod, axis=None):
    """ Mean Gross Error (model and obs unit)"""
    return np.ma.abs(mod - obs).mean(axis=axis)


def MdnE(obs, mod, axis=None):
    """ Median Gross Error (model and obs unit)"""
    return np.ma.median(np.ma.abs(mod - obs), axis=axis)


def NME(obs, mod, axis=None):
    """ Normalized Mean Error (%)"""
    out = (np.ma.abs(mod - obs).sum(axis=axis) / obs.sum(axis=axis)) * 100
    return out


def NMdnE(obs, mod, axis=None):
    """ Normalized Median Error (%)"""
    out = np.ma.median(np.ma.abs(mod - obs), axis=axis) / \
        np.ma.median(obs, axis=axis) * 100
    return out


def FE(obs, mod, axis=None):
    """ Fractional Error (%)"""
    return (np.ma.abs(mod - obs) / (mod + obs)).mean(axis=axis) * 2. * 100.


def MNPB(obs, mod, paxis, axis=None):
    """ Mean Normalized Peak Bias (%)"""
    obsmax = obs.max(axis=paxis)
    return ((mod.max(axis=paxis) - obsmax) / obsmax).mean(axis=axis) * 100.


def MdnNPB(obs, mod, paxis, axis=None):
    """ Median Normalized Peak Bias (%)"""
    obsmax = obs.max(axis=paxis)
    modmax = mod.max(axis=paxis)
    return np.ma.median((modmax - obsmax) / obsmax, axis=axis) * 100.


def MNPE(obs, mod, paxis, axis=None):
    """ Mean Normalized Peak Error (%)"""
    modmax = mod.max(axis=paxis)
    obsmax = obs.max(axis=paxis)
    return ((np.ma.abs(modmax - obsmax)) / obsmax).mean(axis=axis) * 100.


def MdnNPE(obs, mod, paxis, axis=None):
    """ Median Normalized Peak Bias (%)"""
    modmax = mod.max(axis=paxis)
    obsmax = obs.max(axis=paxis)
    pe = np.ma.abs(modmax - obsmax)
    return np.ma.median((pe) / obsmax, axis=axis) * 100.


def NMPB(obs, mod, paxis, axis=None):
    """ Normalized Mean Peak Bias (%)"""
    modmax = mod.max(axis=paxis)
    obsmax = obs.max(axis=paxis)
    return (modmax - obsmax).mean(axis=axis) / obsmax.mean(axis=axis) * 100.


def NMdnPB(obs, mod, paxis, axis=None):
    """ Normalized Median Peak Bias (%)"""
    modmax = mod.max(axis=paxis)
    obsmax = obs.max(axis=paxis)
    return (np.ma.median((modmax - obsmax), axis=axis) /
            np.ma.median(obsmax, axis=axis) * 100.)


def NMPE(obs, mod, paxis, axis=None):
    """ Normalized Mean Peak Error (%)"""
    modmax = mod.max(axis=paxis)
    obsmax = obs.max(axis=paxis)
    return (np.ma.abs(modmax - obsmax).mean(axis=axis) /
            obsmax.mean(axis=axis) * 100.)


def NMdnPE(obs, mod, paxis, axis=None):
    """ Normalized Median Peak Bias (%)"""
    modmax = mod.max(axis=paxis)
    obsmax = obs.max(axis=paxis)
    return (np.ma.median(np.ma.abs(modmax - obsmax), axis=axis) /
            np.ma.median(obsmax, axis=axis) * 100.)


def R2(obs, mod, axis=None):
    """ Coefficient of Determination (unit squared)"""
    from scipy.stats.mstats import pearsonr
    if axis is None:
        return pearsonr(obs, mod)[0]**2
    else:
        r = pearsonr
        return apply_along_axis_2v(lambda x, y: r(x, y)[0]**2, axis, obs, mod)


def RMSE(obs, mod, axis=None):
    """ Root Mean Square Error (model unit)"""
    return np.ma.sqrt(((mod - obs)**2).mean(axis=axis))


def RMSEs(obs, mod, axis=None):
    """Root Mean Squared Error systematic (obs, mod_hat)"""
    from scipy.stats.mstats import linregress
    if axis is None:
        try:
            m, b, rval, pval, stderr = linregress(obs, mod)
            mod_hat = b + m * obs
            return RMSE(obs, mod_hat)
        except ValueError:
            return None
    else:
        myvals = apply_along_axis_2v(
            lambda x, y: linregress(x, y), axis, obs, mod)
        myvals = np.rollaxis(myvals, myvals.ndim - 1, 0).astype(obs.dtype)
        m, b, rval, pval, stderr = myvals
        mod_hat = b + m * obs
        result = RMSE(obs, mod_hat, axis=axis)
        return result


def matchmasks(a1, a2):
    mask = np.ma.getmaskarray(a1) | np.ma.getmaskarray(a2)
    return np.ma.masked_where(mask, a1), np.ma.masked_where(mask, a2)


def matchedcompressed(a1, a2):
    a1, a2 = matchmasks(a1, a2)
    return a1.compressed(), a2.compressed()


def RMSEu(obs, mod, axis=None):
    """Root Mean Squared Error unsystematic (mod_hat, mod)"""
    from scipy.stats.mstats import linregress
    if axis is None:
        try:
            m, b, rval, pval, stderr = linregress(obs, mod)
            mod_hat = b + m * obs
            return RMSE(mod_hat, mod)
        except ValueError:
            return None
    else:
        myvals = apply_along_axis_2v(
            lambda x, y: linregress(x, y), axis, obs, mod)
        myvals = np.rollaxis(myvals, myvals.ndim - 1, 0).astype(obs.dtype)
        m, b, rval, pval, stderr = myvals
        mod_hat = b + m * obs
        result = RMSE(mod_hat, mod, axis=axis)
        return result


def d1(obs, mod, axis=None):
    """ Modified Index of Agreement, d1"""
    return (1.0 -
            np.ma.abs(obs - mod).sum(axis=axis) /
            (np.ma.abs(mod - obs.mean(axis=axis)) +
             np.ma.abs(obs - obs.mean(axis=axis))).sum(axis=axis))


def E1(obs, mod, axis=None):
    """ Modified Coefficient of Efficiency, E1"""
    return (1.0 -
            np.ma.abs(obs - mod).sum(axis=axis) /
            (np.ma.abs(obs - obs.mean(axis=axis))).sum(axis=axis))


def IOA(obs, mod, axis=None):
    """ Index of Agreement, IOA"""
    obsmean = obs.mean(axis=axis)
    if axis is not None:
        obsmean = np.expand_dims(obsmean, axis=axis)
    return (1.0 -
            (np.ma.abs(obs - mod)**2).sum(axis=axis) /
            ((np.ma.abs(mod - obsmean) +
              np.ma.abs(obs - obsmean))**2).sum(axis=axis))