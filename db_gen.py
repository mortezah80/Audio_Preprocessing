from os import listdir
from os.path import isfile, join
import numpy as np
import soundfile as sf
from numpy import random
import audio2numpy as ap
import yaml
import librosa
import os


class DataBaseGenerator:
    def __init__(self, config):
        self.db_address = config['db_address']
        self.aud_path = self.db_address + '/audio'
        self.lab_path = self.db_address + '/lab'
        self.sr = config['sr']
        self.f_name = config['file_name']
        self.num_sample = config['num_sample']
        self.db_name = config['new_db_name']
        self.len_sample = config['len_sample']

    def read_files(self):
        """
        This function reads label file and audio file

        :param aud_path: get audio path. If we do not specify the address, it will look for files in the code execution
         location by default.
        :param lab_path: get label path. If we do not specify the address, it will look for files in the code execution
         location by default.
        :return:
                label_dict : Names of label file in path.
                waveform_dict : A dictionary that keys are the names of the label files, and values are the waveform of
                 the audio file of the label
                label_file_value : A dictionary that keys are the names of the label files, and values of the dictionary
                 are the values of label files which is a list of speech and non_specch times and their categories.

        """
        data_list = []
        label_dict = {}
        waveform_dict = {}
        label_file_value = {}

        aud_files = [f for f in listdir(self.aud_path) if isfile(join(self.aud_path, f))]
        lab_files = [f for f in listdir(self.lab_path) if isfile(join(self.lab_path, f))]

        for f in lab_files:
            if f.split('.')[-1] == 'lab':
                sid = '_'.join(f.split('_')[0:3])
                if sid in label_dict.keys():
                    aud = self.aud_path + '/' + f.strip('.lab') + '.mp3'
                    lab = self.lab_path + '/' + f
                    data_list[label_dict[sid]].append({lab: aud})
                else:
                    aud = self.aud_path + '/' + f.strip('.lab') + '.mp3'
                    lab = self.lab_path + '/' + f
                    s_d = {sid: [len(data_list)]}
                    label_dict[sid] = len(data_list)
                    data_list.append([{lab: aud}])

        for k in label_dict.keys():
            for l in data_list[label_dict[k]]:
                file = open(list(l.keys())[0], "r")
                lab = file.read().split('\n')

                for i in range(0, len(lab)):
                    lab[i] = lab[i].split(' ')
                lab.remove([''])

                if k in label_file_value.keys():
                    label_file_value[k].append(lab)
                else:
                    label_file_value[k] = [lab]
                waveform, _ = ap.open_audio(list(l.values())[0])
                if k in waveform_dict.keys():
                    waveform_dict[k].append(waveform)
                else:
                    waveform_dict[k] = [waveform]
        return label_dict, waveform_dict, label_file_value

    def split_speech_noise(self, label_dict, waveform_dict, label_file_value):
        """
        This function separates speech and noise in the data

        :param label_dict: Names of label file in path.
        :param waveform_dict: A dictionary that keys are the names of the label files, and values are the waveform of
         the audio file of the label
        :param label_file_value: A dictionary that keys are the names of the label files, and values of the dictionary
        are the values of label files which is a list of speech and non_specch times and their categories.
        :return:
                speech : A dictionary that keys are the names of the label files, and values are the waveform of
                the speech segment
                noises : A dictionary that keys are the categories of the noises, and values are the waveform of
                the noise segment
                prob_speech : probability of choosing speech or noise based on the average length of each
                class(speech,noise).
                prob_noise : The list of the probability of choosing each category based on the average length of
                each category.
        """
        sum_speech = 0
        len_speech = 0

        speech = {}
        noises = {'00': [], '01': [], '02': [], '03': [], '04': [], '05': []}
        avg_noise_dict = {
            'avg_noise_0': [0, 0],
            'avg_noise_1': [0, 0],
            'avg_noise_2': [0, 0],
            'avg_noise_3': [0, 0],
            'avg_noise_4': [0, 0],
            'avg_noise_5': [0, 0],
        }

        for k in label_file_value.keys():
            speech[k] = []

        for k in label_dict.keys():
            for l in label_file_value[k]:
                waves = waveform_dict[k][label_file_value[k].index(l)]
                for j in l:
                    if j[2] == '10' or j[2] == '11' or j[2] == '12' or j[2] == '13':
                    # if j[2] == '13' :
                        sum_speech += float(j[1]) - float(j[0])
                        len_speech += 1

                        if j != l[0] and j != l[-1]:
                            temp_d = {}

                            ix = l.index(j)
                            pre = l[ix - 1]
                            post = l[ix + 1]

                            waveform = waves[int(float(pre[0]) * self.sr):int(float(post[1]) * self.sr)]
                            signal = [float(pre[1]) - float(pre[0]), float(j[1]) - float(j[0]) + float(pre[1])
                                      - float(pre[0])]
                            noise = [pre[2], post[2]]
                            temp_d['waveform'] = waveform
                            temp_d['signal'] = signal
                            temp_d['noise'] = noise
                            if signal[1] - signal[0] > 1:
                                speech[k].append(temp_d)

                    elif j[2] == '00':
                        noises['00'].append(waves[int(float(j[0]) * self.sr):int(float(j[1]) * self.sr)])
                        avg_noise_dict['avg_noise_0'][0] += float(j[1]) - float(j[0])
                        avg_noise_dict['avg_noise_0'][1] += 1

                    elif j[2] == '01':
                        noises['01'].append(waves[int(float(j[0]) * self.sr):int(float(j[1]) * self.sr)])
                        avg_noise_dict['avg_noise_1'][0] += float(j[1]) - float(j[0])
                        avg_noise_dict['avg_noise_1'][1] += 1

                    elif j[2] == '02':
                        noises['02'].append(waves[int(float(j[0]) * self.sr):int(float(j[1]) * self.sr)])
                        avg_noise_dict['avg_noise_2'][0] += float(j[1]) - float(j[0])
                        avg_noise_dict['avg_noise_2'][1] += 1

                    elif j[2] == '03':
                        noises['03'].append(waves[int(float(j[0]) * self.sr):int(float(j[1]) * self.sr)])
                        avg_noise_dict['avg_noise_3'][0] += float(j[1]) - float(j[0])
                        avg_noise_dict['avg_noise_3'][1] += 1

                    elif j[2] == '04':
                        noises['04'].append(waves[int(float(j[0]) * self.sr):int(float(j[1]) * self.sr)])
                        avg_noise_dict['avg_noise_4'][0] += float(j[1]) - float(j[0])
                        avg_noise_dict['avg_noise_4'][1] += 1

                    elif j[2] == '05':
                        noises['05'].append(waves[int(float(j[0]) * self.sr):int(float(j[1]) * self.sr)])
                        avg_noise_dict['avg_noise_5'][0] += float(j[1]) - float(j[0])
                        avg_noise_dict['avg_noise_5'][1] += 1

        sum_all_noise = 0
        len_all_noise = 0
        prob_noise = []
        for i in avg_noise_dict.values():
            try:
                prob_noise.append((1 / (i[0] / i[1])))
                sum_all_noise += i[0]
                len_all_noise += i[1]
            except ZeroDivisionError:
                prob_noise.append(0)
        sum_avg = sum(prob_noise)
        for i, j in enumerate(prob_noise):
            if j == 0:
                prob_noise[i] = j
            else:
                prob_noise[i] = (j / sum_avg)

        speech_second_average = sum_speech / len_speech
        noise_second_average = sum_all_noise / len_all_noise
        prob_speech = round(speech_second_average / (noise_second_average + speech_second_average), 2)
        # prob_speech = 0
        return speech, noises, prob_speech, prob_noise

    def augment(self, label_dict, speech, noises, prob_speech, prob_noise, num_sample):
        """

        :param label_dict: Names of label file in path.
        :param speech: A dictionary that keys are the names of the label files, and values are the waveform of
        the speech segment
        :param noises:  A dictionary that keys are the categories of the noises, and values are the waveform of
        the noise segment
        :param prob_speech: probability of choosing speech or noise based on the average length of each
         class(speech,noise).
        :param prob_noise: The list of the probability of choosing each category based on the average length of
        each category.
        :return:
                speechLen : lenght of all speech waveform
                categoriesLen : lenght of all noise waveform
                rttm_label : list of rttm
                audio : list of randomly generated voice
        """
        rttm_label: list = []
        # audio = []
        audio = np.array([])
        categoriesLen: list = []
        speechLen = 0
        n_index = {'00': 0, '01': 1, '02': 2, '03': 3, '04': 4, '05': 5}

        for i in range(len(noises.keys())):
            categoriesLen.append(0)

        while len(audio) / self.sr < self.len_sample:
            # adding speech
            if np.random.random() > prob_speech + 0.09:
                k = random.randint(len(speech.keys()))
                # k = random.randint(3)

                ID = list(label_dict.keys())[list(label_dict.values()).index(k)]
                segment = {"waveform" : []}
                while len(segment['waveform'])== 0 :
                    segment = speech[ID][random.randint(len(speech[ID]))]

                if segment['waveform'].ndim > 1:
                    channel1 = segment['waveform'][:, 0]
                    channel2 = segment['waveform'][:, 1]
                    if channel1.sum() > channel2.sum():
                        # audio.append(channel1)
                        segment['waveform'] = channel1
                    else:
                        segment['waveform'] = channel2

                if (segment['signal'][1] - segment['signal'][0]) > 1:
                    start_0 = str((len(audio)) / self.sr + segment['signal'][0])

                    lab_0 = 'SPEAKER ' + self.f_name + f"{num_sample}" + ' 1 ' + start_0 + ' ' + str(
                        segment['signal'][1] - segment['signal'][0]) + ' <NA> <NA> ' + ID + ' <NA> <NA>'

                    # adding overlap
                    if np.random.random() > 1 :
                        k_o = random.randint(len(speech.keys()))
                        k_o = random.randint(3)

                        if k_o == k:
                            continue
                        ID_o = list(label_dict.keys())[list(label_dict.values()).index(k_o)]
                        segment_o = {"waveform" : []}
                        while len(segment_o['waveform']) == 0:
                            segment_o = speech[ID_o][random.randint(len(speech[ID_o]))]
                        if segment_o['waveform'].ndim > 1:
                            channel1 = segment_o['waveform'][:, 0]
                            channel2 = segment_o['waveform'][:, 1]
                            if channel1.sum() > channel2.sum():
                                # audio.append(channel1)
                                segment_o['waveform'] = channel1
                            else:
                                segment_o['waveform'] = channel2

                        first = segment['waveform']
                        second = segment_o['waveform']
                        print(ID)
                        N = len(first)
                        M = len(second)
                        print("before dead")
                        n = random.randint(N)
                        print("after Dead")
                        m = M - (N - n)
                        k = self.snr_set(first, second, random.randint(0, 10))

                        if m > 0:
                            first = np.concatenate((first, np.zeros(m)))
                            first[n:] = first[n:] + second * k
                            start_1 = str((len(audio) + n) / self.sr + segment_o['signal'][0])

                            lab_1 = 'SPEAKER ' + self.f_name + f"{num_sample}" + ' 1 ' + start_1 + ' ' + str(
                                segment_o['signal'][1] - segment_o['signal'][0]) + ' <NA> <NA> ' + ID_o + ' <NA> <NA>'

                        else:
                            first[n:n + M] = first[n:n + M] + second * k
                            start_1 = str((len(audio) + n) / self.sr + segment_o['signal'][0])

                            lab_1 = 'SPEAKER ' + self.f_name + f"{num_sample}" + ' 1 ' + start_1 + ' ' + str(
                                segment_o['signal'][1] - segment_o['signal'][0]) + ' <NA> <NA> ' + ID_o + ' <NA> <NA>'

                        segment['waveform'] = first

                        if np.random.random() > 0.5:
                            k_o2 = random.randint(len(speech.keys()))
                            # k_o2 = random.randint(3)

                            if k_o2 == k_o or k_o2 == k:
                                continue

                            ID_o2 = list(label_dict.keys())[list(label_dict.values()).index(k_o2)]
                            segment_o2 = {"waveform" : []}
                            while len(segment_o2['waveform']) == 0:
                                segment_o2 = speech[ID_o2][random.randint(len(speech[ID_o2]))]
                            if segment_o2['waveform'].ndim > 1:
                                channel1 = segment_o2['waveform'][:, 0]
                                channel2 = segment_o2['waveform'][:, 1]
                                if channel1.sum() > channel2.sum():
                                    # audio.append(channel1)
                                    segment_o2['waveform'] = channel1
                                else:
                                    segment_o2['waveform'] = channel2

                            first = segment['waveform']
                            second = segment_o2['waveform']
                            N = len(first)
                            M = len(second)
                            n = random.randint(N)
                            m = M - (N - n)
                            k = self.snr_set(first, second, random.randint(0, 10))

                            if m > 0:
                                first = np.concatenate((first, np.zeros(m)))
                                first[n:] = first[n:] + second * k
                                start_2 = str((len(audio) + n) / self.sr + segment_o2['signal'][0])

                                lab_2 = 'SPEAKER ' + self.f_name + f"{num_sample}" + ' 1 ' + start_2 + ' ' + str(
                                    segment_o2['signal'][1] - segment_o2['signal'][0]) + ' <NA> <NA> ' + ID_o2 + \
                                        '<NA> <NA>'

                            else:
                                first[n:n + M] = first[n:n + M] + second * k
                                start_2 = str((len(audio) + n) / self.sr + segment_o2['signal'][0])

                                lab_2 = 'SPEAKER ' + self.f_name + f"{num_sample}" + ' 1 ' + start_2 + ' ' + str(
                                    segment_o2['signal'][1] - segment_o2['signal'][0]) + ' <NA> <NA> ' + ID_o2 + \
                                        '<NA> <NA>'

                            segment['waveform'] = first
                            lab_temp2 = rttm_label.append(lab_2)
                        rttm_label.append(lab_1)
                    rttm_label.append(lab_0)
                    # audio = np.concatenate((audio, segment['waveform']))

                    if segment['waveform'].ndim == 1:
                        segment = segment['waveform'][np.newaxis].T
                        channel1 = segment[:, 0]
                        audio = np.concatenate((audio, channel1))
                        speechLen += len(segment)
                    else:
                        channel1 = segment['waveform'][:, 0]
                        channel2 = segment['waveform'][:, 1]
                        if channel1.sum() > channel2.sum():
                            # audio.append(channel1)
                            audio = np.concatenate((audio, channel1))
                        else:
                            audio = np.concatenate((audio, channel2))
                        speechLen += len(segment['waveform'])

            else:
                k = np.random.choice(len(noises.keys()), 1, p=prob_noise)
                k_n = list(noises.keys())[list(n_index.values()).index(k[0])]
                if len(noises[k_n]) > 0:
                    segment = noises[k_n][random.randint(len(noises[k_n]))]
                    if segment.ndim == 1:
                        segment = segment[np.newaxis].T
                        categoriesLen[int(k_n[1])] += len(segment)
                        channel1 = segment[:, 0]
                        audio = np.concatenate((audio, channel1))
                    else:
                        categoriesLen[int(k_n[1])] += len(segment)
                        channel1 = segment[:, 0]
                        channel2 = segment[:, 1]
                        if channel1.sum() > channel2.sum():
                            audio = np.concatenate((audio, channel1))
                        else:
                            audio = np.concatenate((audio, channel2))

        return speechLen, categoriesLen, rttm_label, audio

    def result(self, speechLen, categoriesLen):
        noisesLen = 0
        for i in categoriesLen:
            noisesLen += i

        allLen = speechLen + noisesLen

        print("Speech: ", round(speechLen * 100 / allLen, 2), " and nonSpeech : ", round(noisesLen * 100 / allLen, 2),
              "%")

        for k in range(len(categoriesLen)):
            if categoriesLen[k] != 0:
                print("category ", k, " is : ", round(categoriesLen[k] * 100 / noisesLen, 2), "%")

    def cal_rms(self, amp):

        return np.sqrt(np.mean(np.square(amp), axis=-1))

    def snr_set(self, signal, noise, snr):
        sig_rms = self.cal_rms(signal)
        noise_rms = self.cal_rms(noise) + 1e-9
        a = float(snr) / 20
        K = sig_rms / (noise_rms * 10 ** a)
        adjusted_noise = noise * K
        # mixed = signal + adjusted_noise
        return K

    def write_rttm(self, rttm_label, num_sample):
        """
        generate rttm file
        """
        rttm_label = sorted(rttm_label, key=lambda x: float(x.split()[3]))
        with open(self.f_name + f"{num_sample}" + '.rttm', 'w') as f:
            for item in rttm_label:
                f.write("%s\n" % item)

    def make_sound(self, audio, num_sample):
        """
        This function makes the mp3 file
        """
        # a = np.asarray(audio[0])
        # for i in range(0, 100):
        #     a = np.concatenate([a, audio[i]])
        # audio = a
        print("made: " ,num_sample)
        audio = librosa.resample(audio, self.sr, 16000)
        sf.write(self.f_name + f"{num_sample}" + '.wav', audio, 16000)
        # AudioSegment.from_wav("sample.wav").export("sample.mp3", format="mp3")

    def __call__(self):
        # folder = os.path.join(self.db_address, self.db_name)
        # os.makedirs(folder)
        # out_file = open(folder, "w")
        for i in range(1, self.num_sample+1):
            label_dict, waveform_dict, label_file_value = self.read_files()
            speech, noises, prob_speech, prob_noise = self.split_speech_noise(label_dict=label_dict,
                                                                              waveform_dict=waveform_dict,
                                                                              label_file_value=label_file_value)
            speechLen, categoriesLen, rttm_label, audio = self.augment(label_dict=label_dict, speech=speech,
                                                                       noises=noises, prob_speech=prob_speech,
                                                                       prob_noise=prob_noise,
                                                                       num_sample=i)
            self.result(speechLen=speechLen, categoriesLen=categoriesLen)
            self.write_rttm(rttm_label=rttm_label, num_sample=i)
            with open('MixHeadset.train.rttm', 'a') as outfile:
                with open(self.f_name + f'{i}' + '.rttm') as infile:
                    for line in infile:
                        outfile.write(line)
                    # os.remove(self.f_name + f'{i}' + '.rttm')
            self.make_sound(audio=audio, num_sample=i)


with open('db_gen.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

np.random.seed(1)
db = DataBaseGenerator(config)
db()
print("end")
