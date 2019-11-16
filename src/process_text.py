import os
import string
from g2p_en import G2p

phones = {}
cmudict = {}

g2p = G2p()

def get_phone_root(phone, sep='_'):
    if not phone or phone == sep:
        return phone

    phone_root = phone.split(sep)[0]
    if phone_root[-1].isdigit():
        return phone_root[:-1]

    return phone_root

with open('filter_phones_small_final.txt') as f:
    for i in f:
        tmp = i.split()
        phones[tmp[0]] = tmp[1].strip()
    last = len(phones)
    phones[' '] = '39'

with open('cmudict.formatted.dict') as f:
    for i, line in enumerate(f):
        tmp = line.split()
        word = tmp[0].lower()
        pron = []
        for p in tmp[1:]:
            if p == '#':
                break
            pron.append(get_phone_root(p))

        cmudict[word] = pron


def g2p_text(text_list):
    wrong, correct = [], []
    for t in text_list:
        token = t.lower()
        if "'" in t and cmudict.get(token):
            wrong.append('|'.join(g2p(t)))
            correct.append('|'.join(cmudict[token]))

    candidate = g2p(' '.join(text_list))
    candidate = '|'.join(candidate)
    for idx, w in enumerate(wrong):
        candidate = candidate.replace(w, correct[idx])

    candidate = candidate.split('|')

    candidate = [get_phone_root(p) for p in candidate if p not in string.punctuation]
    return candidate


dur = {}
with open('utt2dur') as f:
    for i in f:
        tmp = i.split()
        dur[tmp[0]] = tmp[1].strip()

wav = {}
with open('wav.scp') as f:
    for i in f:
        tmp = i.strip().split()
        filepath = ' '.join(tmp[1:])
        filepath = filepath.replace('/home/eflsd/storage/pitch_data', '/home/eflsd/storage/audio_data/pitch_data')
        filepath = filepath.replace('/home/eflsd/dev/asr_training_data', '/home/eflsd/storage/audio_data/asr_training_data')
        filepath = filepath.replace('/home/eflsd/dev/Projects/librispeech/data/', '/home/eflsd/storage/audio_data/')
        filepath = filepath.replace('//', '/')
        if 'flac' in filepath:
            filepath = filepath.replace('flac -c -d -s ', '').replace('.flac |', '.wav').replace('LibriSpeech', 'LibriSpeech_wav')
        if not os.path.exists(filepath):
            raise Exception(f'failed file assertion, {filepath}')
        wav[tmp[0]] = filepath

with open('text') as f:
    for i in f:
        tmp = i.split()
        filename = tmp[0]
        seq = g2p_text(tmp[1:])
        seq_id = [phones[p] for p in seq]

        #print(tmp[1:], seq, seq_id)
        print('{},{},{}'.format(wav[filename], dur[filename], ' '.join(seq_id)))


