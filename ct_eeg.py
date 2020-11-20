from mne.preprocessing import ICA
from mne.preprocessing import create_eog_epochs
from glob import glob
from alpha_trigger_locations import locations
import re
import mne
import csv
import numpy
import pandas
import matplotlib.pyplot as plt
import philistine as phil
import traceback

participants = {
    'P1': [],
    'P2': [],
    'P3': [],
    'P5': [],
    'P6': [],
    'P7': [],
    'P8': [],
    'P9': [],
    'P10': [],
    'P11': [],
    'P12': [],
    'P13': [],
    'P14': [],
    'P15': [],
    'P16': [],
    'P17': [],
    'P18': [],
    'P19': [],
    'P20': [],
    'P21': [],
    'P22': [],
    'P23': [],
    'P24': [],
    'P25': [],
    'P26': [],
    'P27': [],
    'P28': [],
    'P29': [],
    'P30': [],
    'P31': [],
    'P32': [],
    'P33': [],
    'P34': [],
    'P35': [],
    'P36': [],
    'P37': [],
    'P38': [],
    'P39': [],
    'P40': [],
    'P41': [],
    'P42': [],
    'P43': [],
    'P44': [],
    'P45': [],
    'P46': [],
}

trigger_codes = {
    'S2-EO1': 210,
    'S2-EC1': 220,
    'S2-CT': 230,
    'S2-EO2': 240,
    'S2-EC2': 250,
    'S5-EO1': 510,
    'S5-EC1': 520,
    'S5-CT': 530,
    'S5-EO2': 540,
    'S5-EC2': 550,
}


class Participant:
    def __init__(self, pid: str, filename: str):
        self.pid = pid
        self.filename = filename
        self.bads = participants[pid]

        if 'S2' in filename:
            self.event_id = dict((k, trigger_codes[k]) for k in ('S2-EO1', 'S2-EC1', 'S2-CT', 'S2-EO2', 'S2-EC2'))
        else:
            self.event_id = dict((k, trigger_codes[k]) for k in ('S5-EO1', 'S5-EC1', 'S5-CT', 'S5-EO2', 'S5-EC2'))
        self.events = numpy.empty(1)

    def preprocess(self):
        raw_file = 'Cognitive Training/' + self.filename + '.vhdr'
        outfile = 'Cognitive Training/processed/' + self.filename + '.raw.fif'

        raw: mne.io.Raw = mne.io.read_raw_brainvision(raw_file,
                                                      preload=True)
        raw = mne.set_eeg_reference(raw, ref_channels=['TP9', 'TP10'])[0]
        raw.drop_channels(['TP9', 'TP10'])  # Re-reference channels
        raw.drop_channels(['Fz', 'F3', 'F7', 'FT9', 'FC5', 'FC1', 'C3', 'T7', 'CP5', 'CP1', 'P7',
                           'P8', 'CP6', 'CP2', 'Cz', 'C4', 'T8', 'FT10', 'FC6',
                           'FC2', 'F4', 'F8'])  # Only interested in P3, Pz, P4, O1, Oz, O2
        mne.set_bipolar_reference(raw, anode=['Fp1'], cathode=['Fp2'], ch_name=['EOG'], copy=False)
        raw.set_channel_types({'EOG': 'eog'})

        montage = mne.channels.make_standard_montage('standard_1020')
        raw.set_montage(montage)

        # self.compute_ica_correction(raw)  # ICA not needed as EOG artifacts do not impact O/P electrodes

        raw = raw.filter(0.1, 30,
                         phase='zero',
                         method='fir',
                         l_trans_bandwidth='auto',
                         h_trans_bandwidth='auto')

        raw.save(outfile, overwrite=True)

    def generate_events(self):
        raw_file = 'Cognitive Training/processed/' + self.filename + '.raw.fif'
        raw: mne.io.Raw = mne.io.read_raw_fif(raw_file,
                                              preload=True)

        if 'S2' in self.filename:
            keys = locations[self.pid][:5]
        else:
            keys = locations[self.pid][5:]

        events = []
        index_modifier = 0
        for index, value in enumerate(list(keys)):
            if value[0] == -1:
                del keys[index-index_modifier]
                del self.event_id[list(self.event_id.keys())[index-index_modifier]]
                index_modifier += 1
            else:
                # Generate the events
                temp = mne.make_fixed_length_events(raw,
                                                    id=self.event_id[list(self.event_id.keys())[index-index_modifier]],
                                                    duration=2.0,
                                                    start=raw.annotations.onset[value[0]-1],
                                                    stop=raw.annotations.onset[value[1]-1],
                                                    first_samp=False)
                events.append(temp)
        events = numpy.concatenate(events)
        self.events = events[events[:, 0].argsort()]

    def extract_epochs(self):
        raw = mne.io.read_raw_fif('Cognitive Training/processed/{0}.raw.fif'.format(self.filename), preload=True)
        tmin = 0
        tmax = 2

        raw.info['bads'] = participants[self.pid]
        if len(raw.info['bads']) > 0:
            raw.interpolate_bads(reset_bads=True)

        picks = mne.pick_types(raw.info, meg=False, eeg=True, eog=True, stim=False, exclude='bads')
        reject = dict(eeg=150e-6)
        flat = dict(eeg=5e-6)
        epochs = mne.Epochs(raw, self.events, event_id=self.event_id,
                            tmin=tmin, tmax=tmax,
                            proj=False, picks=picks,
                            baseline=None,
                            detrend=0,  # DC offset
                            reject_by_annotation=False,
                            flat=flat,
                            reject=reject,
                            preload=True)
        bad_epoch_mask = phil.mne.abs_threshold(epochs, 75e-6)
        epochs.drop(bad_epoch_mask, reason="absolute threshold")
        try:
            rejections = epochs.plot_drop_log(show=True)
            rejections.savefig('Cognitive Training/figures/{0}_dropped.png'.format(self.filename))
        except Exception:
            print(self.filename, 'has no drops!')

        try:
            epochs.save('Cognitive Training/epochs/{0}-epo.fif'.format(self.filename), overwrite=True)
        except IndexError:
            print('Participant {0} skipped for no epochs'.format(self.filename))

    def time_frequency(self):
        iaf_file = 'iaf/' + self.pid + '_iaf_long.txt'
        iaf_info = pandas.read_table(iaf_file,
                                     dtype={'pid': numpy.str, 'session': numpy.str, 'measure': numpy.str,
                                            'value': numpy.float64},
                                     na_values='None', sep=' ')
        iaf_info_means = iaf_info.groupby(['pid', 'measure'], as_index=False).agg('mean')
        epochs = mne.read_epochs('Cognitive Training/epochs/' + self.filename + '-epo.fif')

        tf_all: pandas.DataFrame = pandas.DataFrame()
        bands = ['alpha', 'theta']
        windows = {
            'pre': (-300, 300),
            'slice': (300, 1700),
            'post': (1700, 2300)
        }

        for b in bands:
            print('processing ' + b + ' band')
            band_lower = b + '_' + 'lower'
            band_upper = b + '_' + 'upper'

            lower = float(iaf_info_means.value[iaf_info_means['measure'] == band_lower])
            upper = float(iaf_info_means.value[iaf_info_means['measure'] == band_upper])

            freqs = numpy.linspace(lower, upper, 5)
            ncycles = freqs / 4
            tf_list = []

            self.event_id = epochs.event_id

            try:
                for x in self.event_id:
                    print("processing " + x)
                    tfreq = mne.time_frequency.tfr_array_morlet(epochs[x].get_data(), sfreq=epochs[x].info['sfreq'],
                                                                freqs=freqs,
                                                                n_cycles=ncycles, output='power')
                    df = pandas.DataFrame(numpy.column_stack(
                        list(map(numpy.ravel, numpy.meshgrid(*map(numpy.arange, tfreq.shape), indexing="ij"))) + [
                            tfreq.ravel()]),
                        columns=['epoch', 'channel', 'frequency', 'time', 'power'])
                    df['pid'] = self.pid
                    df['cond'] = x
                    df['iaf'] = float(iaf_info_means.value[iaf_info_means['measure'] == 'paf'])
                    if 'S2' in self.filename:
                        df['session'] = 'S2'
                    else:
                        df['session'] = 'S5'
                    df['band'] = b
                    tf_list.append(df)

                tf_all = pandas.concat(tf_list)
                tf_all_wins = self.add_windows(tf_all, epochs.tmin, epochs.tmax, windows, epochs.info['sfreq'])
                tf_all_sel = tf_all_wins.drop(['frequency', 'time'], axis=1)
                tf_means = tf_all_sel.groupby(['epoch', 'cond', 'channel', 'pid', 'win', 'session', 'band'], as_index=False).agg('mean')
                tf_means['ch_name'] = tf_means.apply(lambda row: self.get_channel_name(epochs, int(row['channel'])), axis=1)
                tf_means.to_csv('Cognitive Training/time_freq/{0}_{1}.csv'.format(self.pid, b), index=False)
            except ValueError:
                print(self.filename, x, 'Error, skipped')

    @staticmethod
    def add_windows(tf, epoch_tmin, epoch_tmax, windows, sfreq):
        zero_ms = (0 - epoch_tmin) * sfreq

        tf['win'] = 'none'

        for w in windows:
            name = w
            start = windows[w][0]
            stop = windows[w][1]
            if start < 0:
                start_sample = int((zero_ms - abs(start)) / 1000 * sfreq)
            else:
                start_sample = int((zero_ms + start) / 1000 * sfreq)
            if stop < 0:
                stop_sample = int((zero_ms - abs(stop)) / 1000 * sfreq)
            else:
                stop_sample = int((zero_ms + stop) / 1000 * sfreq)

            mask = (tf['time'] > (start_sample - 1)) & (tf['time'] < (stop_sample - 1))
            tf.loc[mask, 'win'] = name

        mask_drop = tf['win'] != 'none'
        tf_wins = tf.loc[mask_drop,]

        return tf_wins

    @staticmethod
    def get_channel_name(epochs, ch_number):
        ch_name = epochs.ch_names[ch_number]
        return ch_name


filenames = glob('Cognitive Training/*.vhdr')

for f in filenames:
    exp = re.search(r"(P\d{1,2})_", f)
    pid = exp.group(1)
    exp = re.search(r"\/(\w*).vhdr", f)
    filename = exp.group(1)
    p = Participant(pid, filename)
    p.preprocess()
    p.generate_events()
    p.extract_epochs()
    p.time_frequency()

# exit(0)
# Combine into one csv
csvs = glob('Cognitive Training/time_freq/*alpha.csv')
dfs = []
for file in csvs:
    df = pandas.read_csv(file, index_col=False)
    dfs.append(df)
joined_frame = pandas.concat(dfs, ignore_index=True)
joined_frame.to_csv('Cognitive Training/time_freq/alpha_combined.csv')

csvs = glob('Cognitive Training/time_freq/*theta.csv')
dfs = []
for file in csvs:
    df = pandas.read_csv(file, index_col=False)
    dfs.append(df)
joined_frame = pandas.concat(dfs, ignore_index=True)
joined_frame.to_csv('Cognitive Training/time_freq/theta_combined.csv')

csvs = glob('Cognitive Training/time_freq/*_combined.csv')
dfs = []
for file in csvs:
    if 'alpha_theta' in file:
        continue
    df = pandas.read_csv(file, index_col=False)
    dfs.append(df)
joined_frame = pandas.concat(dfs, ignore_index=True)
joined_frame.to_csv('Cognitive Training/time_freq/alpha_theta_combined.csv')
