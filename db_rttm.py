from pydub import AudioSegment
import re



# with open('/home/aibox/workstation/afshin/own_file/tets/out_2ordi/annot.txt') as r:
#     l = r.readlines()
#     l2 = []
#     for i in range(len(l)-1):
#         t1 = float(re.sub('\n', '', l[i].split(" ")[1]))
#         t2 = float(re.sub('\n', '', l[i + 1].split(" ")[0]))
#         temp = [t1, t2]
#         l2.append(temp)
#         print(l[i])
#     with open('/home/aibox/workstation/afshin/own_file/tets/out_2ordi/annot_noise.txt', "w") as n:
#         for item in l2:
#             n.write(f'{item[0]} {item[1]}\n')
#     n.close()




audio = AudioSegment.empty()
sound = AudioSegment.from_file("/home/aibox/workstation/afshin/sound.wav", "wav")
with open('/home/aibox/workstation/afshin/voicefactory-SpeechProcessingUnit-master/audio_noise.txt') as r:
    l = r.readlines()
    for i in l:
        temp = i.split(" ")
        StrtTime = float(temp[0])*1000
        EndTime = float(re.sub('\n', '', temp[1]))*1000
        extract = sound[StrtTime:EndTime]
        audio += extract


audio.export("/home/aibox/workstation/afshin/own_file/tets/out_2ordi/our_audio_noise6.wav", format="wav")

