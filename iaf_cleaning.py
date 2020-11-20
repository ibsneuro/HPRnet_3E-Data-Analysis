from glob import glob
import mne

iaf_sections = {
    # 'P1': [(9, 12), (24, 25)],
    # 'P2': [(12, 13), (16, 17)],
    # 'P3': [(7, 8), (196, 197)],
    # 'P5': [(3, 4), (7, 8)],
    # 'P6': [(3, 4), (7, 8)],
    # 'P7': [(3, 4), (7, 8)],
    # 'P8': [(4, 5), (22, 24)],
    # 'P9': [(3, 4), (62, 125)],
    # 'P10': [(3, 4), (7, 8)],
    # 'P11': [(3, 83), (222, 223)],
    # 'P12': [(3, 4), (62, 77)],
    # 'P13': [(42, 43), (55, 56)],
    # 'P14': [(3, 4), (7, 8)],
    # 'P15': [(20, 35), (46, 47)],
    # 'P16': [(3, 4), (7, 8)],
    # 'P17': [(3, 4), (7, 8)],
    # 'P18': [(3, 4), (7, 8)],
    # 'P19': [(3, 4), (7, 8)],
    # 'P20': [(3, 4), (7, 8)],
    # 'P21': [(3, 4), (7, 8)],
    # 'P22': [(3, 4), (7, 8)],
    # 'P23': [(4, 5), (9, 10)],
    # 'P24': [(3, 4), (7, 8)],
    # 'P25': [(3, 4), (7, 8)],
    # 'P26': [(3, 4), (7, 8)],
    # 'P27': [(3, 4), (8, 9)],
    # 'P28': [(3, 4), (7, 8)],
    # 'P29': [(3, 4), (7, 8)],  # No S2, had to use S5
    # 'P30': [(3, 4), (8, 9)],
    # 'P31': [(3, 4), (7, 8)],
    'P32': [(3, 4), (7, 8)],
    'P33': [(3, 4), (7, 8)],
    'P34': [(3, 4), (7, 8)],
    'P35': [(3, 4), (7, 8)],
    'P36': [(3, 4), (7, 8)],
    'P37': [(3, 4), (7, 8)],
    'P38': [(3, 4), (7, 8)],
    'P39': [(3, 4), (7, 8)],
    'P40': [(3, 4), (7, 8)],
    'P41': [(3, 4), (7, 8)],
    'P42': [(3,4), (13,14)],
    'P43': [(3, 4), (7, 8)],
    'P44': [(3, 4), (7, 8)],
    'P45': [(3, 4), (7, 8)],
    'P46': [(3, 4), (7, 8)],
}


def create_iaf_files():
    for pid in iaf_sections.keys():
        if pid == 'P29':
            header = 'P29_S5_CT.vhdr'
        else:
            header = pid + '_S2_CT.vhdr'
        header = 'Cognitive Training/' + header

        raw: mne.io.Raw = mne.io.read_raw_brainvision(header,
                                                      eog=('Fp1', 'Fp2'),
                                                      preload=True)
        m1 = iaf_sections[pid][0][0] - 1
        m2 = iaf_sections[pid][0][1] - 1
        ec1 = raw.copy().crop(tmin=raw._annotations.onset[m1],
                              tmax=raw._annotations.onset[m2],
                              include_tmax=True)
        ec1.plot()
        ec1.save('iaf/raw/{0}_EC1.raw.fif'.format(pid), overwrite=True)

        m1 = iaf_sections[pid][1][0] - 1
        m2 = iaf_sections[pid][1][1] - 1
        ec2 = raw.copy().crop(tmin=raw._annotations.onset[m1],
                              tmax=raw._annotations.onset[m2],
                              include_tmax=True)
        ec2.plot()
        ec2.save('iaf/raw/{0}_EC2.raw.fif'.format(pid), overwrite=True)


create_iaf_files()
