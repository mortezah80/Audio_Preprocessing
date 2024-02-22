import os
import math
from os import listdir
from os.path import isfile, join
from shutil import copyfile

import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import audioop as ap
import pyannote.core
import pyannote.audio
from struct import unpack
import torchaudio as TA
import soundfile as sf
import torch
from soundfile import SoundFile

import urllib
import scipy.io.wavfile
import pydub

import librosa

cwd = os.getcwd()
mypath = cwd
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)

rttm = []
uem = []
for f in onlyfiles:
    if f.split('.')[-1] == 'lab':
        file = open(f, "r")
        print(f)
        lab = file.read().split('\n')

        for i in range(0, len(lab)):
            lab[i] = lab[i].split(' ')
        lab.remove([''])

        for i in lab:
            if int(i[2]) == 10 or int(i[2]) == 11:
                rttm.append('SPEAKER ' + f.rstrip('.lab') + ' 1 ' + i[0] + ' ' + str(float(i[1]) - float(i[0])) +
                            ' <NA> <NA> ' + f.split('.')[0] + ' <NA> <NA>')

        uem.append(f.rstrip('.lab') + ' 1 ' + '0.000 ' + lab[-1][1])

# with open('test.rttm', 'w') as f:
#     for item in rttm:
#         f.write("%s\n" % item)

with open('train.uem', 'w') as f:
    for item in uem:
        f.write("%s\n" % item)