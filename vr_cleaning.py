from glob import glob
import mne

channel_names = {
    'Channel 1,': 'Fp1',
    'Channel 2,': 'Fz',
    'Channel 3,': 'F3',
    'Channel 4,': 'F7',
    'Channel 5,': 'FT9',
    'Channel 6,': 'FC5',
    'Channel 7,': 'FC1',
    'Channel 8,': 'C3',
    'Channel 9,': 'T7',
    'Channel 10,': 'TP9',
    'Channel 11,': 'CP5',
    'Channel 12,': 'CP1',
    'Channel 13,': 'Pz',
    'Channel 14,': 'P3',
    'Channel 15,': 'P7',
    'Channel 16,': 'O1',
    'Channel 17,': 'Oz',
    'Channel 18,': 'O2',
    'Channel 19,': 'P4',
    'Channel 20,': 'P8',
    'Channel 21,': 'TP10',
    'Channel 22,': 'CP6',
    'Channel 23,': 'CP2',
    'Channel 24,': 'Cz',
    'Channel 25,': 'C4',
    'Channel 26,': 'T8',
    'Channel 27,': 'FT10',
    'Channel 28,': 'FC6',
    'Channel 29,': 'FC2',
    'Channel 30,': 'F4',
    'Channel 31,': 'F8',
    'Channel 32,': 'Fp2'
}


def rename_channels():
    files = glob('VR Task/Block*/*.vhdr') + glob('VR Task/Tone Only/*.vhdr')
    for path in files:
        filename = path.split('/')[2]
        block = filename.split('_')[2].split('-')[0]
        with open(path) as file, open('VR Task/rename/' + block + '/' + filename, 'w') as new_file:
            for line in file.readlines():
                new_line = ''
                for key in channel_names.keys():
                    if key in line:
                        name = channel_names[key]
                        new_line = line.replace(key[:-1], name)
                        new_file.write(new_line)
                        break
                if new_line == '':
                    new_file.write(line)


def remove_trailing_comma():
    files = glob('VR Task/Block*/*.vhdr') + glob('VR Task/Tone Only/*.vhdr')
    for path in files:
        filename = path.split('/')[2]
        block = filename.split('_')[2].split('-')[0]
        with open(path) as file, open('VR Task/rename/' + block + '/' + filename, 'w') as new_file:
            for line in file.readlines():
                new_line = ''
                if ',,' in line:
                    new_line = line.replace(',\n', '\n')
                    new_file.write(new_line)
                else:
                    new_file.write(line)


def remove_ch33():
    files = glob('VR Task/Block*/*.vhdr') + glob('VR Task/Tone Only/*.vhdr')
    for path in files:
        filename = path.split('/')[2]
        block = filename.split('_')[2].split('-')[0]
        with open(path) as file, open('VR Task/rename/' + block + '/' + filename, 'w') as new_file:
            for line in file.readlines():
                new_line = ''
                if 'Channel 33' in line:
                    continue
                else:
                    new_file.write(line)


def fix_file_paths():
    headers = glob('VR Task/Block*/*.vhdr') + glob('VR Task/Tone Only/*.vhdr')
    markers = glob('VR Task/Block*/*.vmrk') + glob('VR Task/Tone Only/*.vmrk')

    for header in headers:
        filename = header.split('/')[2]
        block = filename.split('_')[2].split('-')[0]
        with open(header) as infile, open('VR Task/rename/' + block + '/' + filename, 'w') as outfile:
            for line in infile.readlines():
                if 'C:/Users/User/Desktop/ShootingGalleryVR/EEG_LOGS/' in line:
                    outfile.write(line.replace('C:/Users/User/Desktop/ShootingGalleryVR/EEG_LOGS/', ''))
                else:
                    outfile.write(line)

    for marker in markers:
        filename = marker.split('/')[2]
        block = filename.split('_')[2].split('-')[0]
        with open(marker) as infile, open('VR Task/rename/' + block + '/' + filename, 'w') as outfile:
            for line in infile.readlines():
                if 'C:/Users/User/Desktop/ShootingGalleryVR/EEG_LOGS/' in line:
                    outfile.write(line.replace('C:/Users/User/Desktop/ShootingGalleryVR/EEG_LOGS/', ''))
                else:
                    outfile.write(line)


def fix_number_chans():
    files = glob('VR Task/Block*/*.vhdr') + glob('VR Task/Tone Only/*.vhdr')
    for path in files:
        filename = path.split('/')[2]
        block = filename.split('_')[2].split('-')[0]
        with open(path) as file, open('VR Task/rename/' + block + '/' + filename, 'w') as new_file:
            for line in file.readlines():
                if 'NumberOfChannels' in line:
                    new_file.write('NumberOfChannels=32\n')
                else:
                    new_file.write(line)


def all_at_once():
    files = glob('VR Task/Block*/*.vhdr') + glob('VR Task/Tone Only/*.vhdr')
    for path in files:
        filename = path.split('/')[2]
        block = filename.split('_')[2].split('-')[0]
        with open(path) as file, open('VR Task/rename/' + block + '/' + filename, 'w') as new_file:
            for line in file.readlines():
                new_line = ''
                for key in channel_names.keys():
                    if key in line:
                        name = channel_names[key]
                        new_line = line.replace(key[:-1], name)
                        new_line = new_line.replace(',\n', '\n')
                        new_file.write(new_line)
                        break
                if 'Channel 33' in line:
                    continue
                if 'NumberOfChannels' in line:
                    new_file.write('NumberOfChannels=32\n')
                    continue
                if new_line == '':
                    new_file.write(line)


# fix_file_paths()
# rename_channels()
# remove_trailing_comma()
# remove_ch33()
# fix_number_chans()
all_at_once()
