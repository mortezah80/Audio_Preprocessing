import os
from mutagen.mp3 import MP3
# entries = os.scandir(r'/home/aibox/workstation/afshin/pyannot_v2/own_file/sony_rttm')
# for i in entries:
#     with open('/home/aibox/workstation/afshin/pyannot_v2/own_file/sony_rttm/MixHeadset.train.rttm', 'a') as outfile:
#         with open(f'/home/aibox/workstation/afshin/pyannot_v2/own_file/sony_rttm/{i.name}') as infile:
#             for line in infile:
#                 outfile.write(line)

#
entries = os.scandir('/home/aibox/workstation/afshin/data/Sony1Labs-20230131T093458Z-001/Sony1Labs/lab')
segments_list = []
with open('/home/aibox/workstation/afshin/data/Sony1Labs-20230131T093458Z-001/Sony1Labs/all_uem.txt', 'w') as outfile:
    for i in entries:
        print(i.name.split(".")[0])
        temp = i.name.split(".")[0]

        audio = MP3(f"/home/aibox/workstation/afshin/data/Sony1Labs-20230131T093458Z-001/Sony1Labs/audio/{temp}.mp3")
        print(audio.info.length)
        temp += " 1 0.000 " + str(audio.info.length) + '\n'
        outfile.write(temp)




