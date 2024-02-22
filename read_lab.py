import os

final_result = {'total': 0, 'correct': 0, 'missed detection': 0, 'false alarm': 0, 'diarization error rate': 0}

results= []


entries = os.scandir(r'/home/aibox/workstation/afshin/pyannot_v2/own_file/Sony1Labs/test/lab')
sampleNumbers = 23

for i in entries:

    sample_name = i.name
    segments = open(f"/home/aibox/workstation/afshin/pyannot_v2/own_file/Sony1Labs/test/outpts/seg/new_sony/{i.name.split('.')[0]}.mp3.txt", "r")
    segment = segments.readline()
    segments_list = []
    jam = 0
    while segment:
        temp = segment.split(" ")
        start = float(temp[0])
        end = float(temp[1])
        jam += end - start
        segments_list.append((start, end))
        segment = segments.readline()
    print(segments_list)

    segments_sec = segments_list
    # print(segments_sec)
    segments_sec_union = []
    # print(sorted(segments_sec))
    for begin, end in sorted(segments_sec):
        if segments_sec_union and segments_sec_union[-1][1] >= begin - 0:
            segments_sec_union[-1][1] = max(segments_sec_union[-1][1], end)
        else:
            segments_sec_union.append([begin, end])


    print(segments_sec_union)

    segments_rttm = open(f"/home/aibox/workstation/afshin/pyannot_v2/own_file/Sony1Labs/test/lab/{i.name}", "r")
    segment_rttm = segments_rttm.readline()

    segments_rttm_list = []
    jam = 0
    while segment_rttm:
        temp = segment_rttm.split(" ")
        start = float(temp[0])
        end = float(temp[1])
        jam += end - start
        speechOrNot = int(temp[2][0])
        if speechOrNot:
            segments_rttm_list.append((start, end))
        segment_rttm = segments_rttm.readline()

    print(segments_rttm_list)

    segments_lab = segments_rttm_list

    segments_lab_union = []
    # print(sorted(segments_sec))
    for begin, end in sorted(segments_lab):
        if segments_lab_union and segments_lab_union[-1][1] >= begin - 0:
            segments_lab_union[-1][1] = max(segments_lab_union[-1][1], end)
        else:
            segments_lab_union.append([begin, end])

    print(segments_lab_union)
    segments_rttm_list_union = segments_lab_union
    print("------------------------------")


    from pyannote.core import Annotation, Segment

    reference = Annotation()

    for j in segments_rttm_list_union :
        reference[Segment(j[0], j[1])] = 's'

    # print(reference)

    # print("-----------------------------------")
    hypothesis = Annotation()

    for k in segments_sec_union :
        hypothesis[Segment(k[0], k[1])] = 'S'

    # print(hypothesis)


    from pyannote.metrics.diarization import DiarizationErrorRate
    diarizationErrorRate = DiarizationErrorRate()
    result = diarizationErrorRate(reference, hypothesis, detailed=True, uem=Segment(0, segments_rttm_list_union[-1][1]))
    results.append((f"{sample_name}" , result))
    final_result['total'] += result['total']
    final_result['correct'] += result['correct']
    final_result['missed detection'] += result['missed detection']
    final_result['false alarm'] += result['false alarm']
    final_result['diarization error rate'] += result['diarization error rate']

final_result['diarization error rate'] = final_result['diarization error rate'] / sampleNumbers

for i in results:
    print(i)

print("final result : " ,final_result)