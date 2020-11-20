import re
from glob import glob
from philistine.mne import savgol_iaf
import mne
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Electrodes to consider for IAF calculation
electrodes = ['P3', 'Pz', 'P4', 'O1', 'Oz', 'O2']

# Frequency bands to adjust
bands = ['alpha', 'l_alpha', 'u_alpha', 'theta', 'beta']

# Participant IDs
participants = [  # 'P1', 'P2', 'P3', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13',
                  # 'P14', 'P15', 'P16', 'P17', 'P18', 'P19', 'P20', 'P21', 'P22', 'P23', 'P24',
                  # 'P25', 'P26', 'P27', 'P28', 'P29', 'P30', 'P31',
                'P32', 'P33', 'P34', 'P35',
                'P36', 'P37', 'P38', 'P39', 'P40', 'P41', 'P42', 'P43', 'P44', 'P45', 'P46']


def get_freq_band_limits(band, paf):
    """Adjust frequency bands using IAF.
    Uses the golden mean-based algorithm outlined in Klimesch (2012).
    """
    # Golden mean constant
    g = 1.618
    paf_delta = paf / 4
    paf_theta = paf / 2
    paf_beta = paf * 2
    paf_gamma = paf * 4
    lower = 0
    upper = 0
    if band == "alpha":
        lower = round(paf_theta * g, 1)
        upper = round(paf_beta / g, 1)
    elif band == "l_alpha":
        lower = round(paf_theta * g, 1)
        upper = paf
    elif band == "u_alpha":
        lower = paf
        upper = round(paf_beta / g, 1)
    elif band == "theta":
        lower = round(paf_delta * g, 1)
        upper = round(paf / g, 1)
    elif band == "beta":
        lower = round(paf * g, 1)
        upper = round(paf_gamma / g, 1)

    return lower, upper


def iaf(participant, filename, session):
    outfile = open('iaf/{0}_{1}_iaf_long.txt'.format(participant, session), 'w')
    header = "pid" + "\t" + "session" + "\t" + "measure" + "\t" + "value" + "\n"
    outfile.write(header)

    raw = mne.io.read_raw_fif(filename,
                              preload=True)
    # montage = mne.channels.make_standard_montage('standard_1020')
    # raw.set_montage(montage)
    picks = []
    for e in electrodes:
        index = raw.ch_names.index(e)
        picks.append(index)

    # Get IAF
    paf, cog, ablimits = savgol_iaf(raw, picks=picks, fmin=7, fmax=13)
    plt.savefig('iaf/plots/{0}_{1}.png'.format(participant, session))

    outfile.write(participant + "\t" + session + "\t" + "paf\t" + str(paf) + "\n")
    outfile.write(participant + "\t" + session + "\t" + "cog\t" + str(cog) + "\n")

    # Calculate adjusted frequency band limits
    for b in bands:
        band_lower = b + "_" + "lower"
        band_upper = b + "_" + "upper"
        try:
            lower, upper = get_freq_band_limits(b, paf)
        except TypeError:
            lower = "None"
            upper = "None"
        outfile.write(participant + "\t" + session + "\t" + band_lower + "\t" + str(lower) + "\n")
        outfile.write(participant + "\t" + session + "\t" + band_upper + "\t" + str(upper) + "\n")
    outfile.close()


filenames = glob('iaf/raw/*.fif')

for f in filenames:
    exp = re.search(r"[P](\d{1,2})_", f)
    pid = exp.group(1)

    if 'P' + pid not in participants:
        continue

    if 'EC1' in f:
        ses = '1'
    else:
        ses = '2'
    iaf(pid, f, ses)

# Join the two sessions
for p in participants:
    session_files = glob('iaf/{0}_*.txt'.format(p.replace('P', '')))
    dfs = []
    for file in session_files:
        iaf_info = pd.read_table(file, dtype={'pid': np.str, 'session': np.str, 'measure': np.str, 'value': np.float64},
                                 na_values='None')
        dfs.append(iaf_info)
    joined_frame: pd.DataFrame = pd.concat(dfs, ignore_index=True)
    joined_frame.to_csv('iaf/{0}_iaf_long.txt'.format(p), index=False, sep=' ')

