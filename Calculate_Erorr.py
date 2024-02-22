from pyannote.core import Annotation, Segment
from pyannote.metrics.diarization import DiarizationErrorRate

final_result = {'total': 0, 'correct': 0, 'missed detection': 0, 'false alarm': 0, 'diarization error rate': 0}
results = []


sampleNumbers =1
# reading predicted segments
for audioNumber in range(1, sampleNumbers+1):
    segments = open(f"sample{audioNumber}.mp3.txt", "r")
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

    # print("this is jam " , jam)

    # print(segments_list)
    # print()
    # segments_sec = []
    # for segment in segments:
    #     temp = segment.split(" ")
    #     # print(segment)
    #     # print("this is temp " , temp)
    #     start = temp[1]
    #     end = temp[4]
    #     end = end[0:len(end)-1]
    #     # print(start)
    #     # print(end)
    #     temp = start.split(":")
    #     # print(temp)
    #     start = int(temp[0]) * 3600 + int(temp[1])*60 + float(temp[2])
    #     temp = end.split(":")
    #     end = int(temp[0]) * 3600 + int(temp[1])*60 + float(temp[2])
    #     segments_sec.append((start , end))

    segments_sec = segments_list
    # print(segments_sec)
    segments_sec_union = []
    # print(sorted(segments_sec))
    for begin, end in sorted(segments_sec):
        if segments_sec_union and segments_sec_union[-1][1] >= begin - 0:
            segments_sec_union[-1][1] = max(segments_sec_union[-1][1], end)
        else:
            segments_sec_union.append([begin, end])

    # print("this is :   " ,segments_sec_union)

    # reading rttm segments
    segments_rttm = open(f"Sony1lab_rttms_6h/sample{audioNumber}.rttm", "r")
    segment_rttm = segments_rttm.readline()
    segments_rttm_list = []
    while segment_rttm:
        temp = segment_rttm.split(" ")
        start = float(temp[3])
        end = start + float(temp[4])
        segments_rttm_list.append((start, end))
        segment_rttm = segments_rttm.readline()

    # print(segments_rttm_list)
    # print()
    # print()
    segments_rttm_list_union = []
    # print(sorted(segments_rttm_list))
    for begin, end in sorted(segments_rttm_list):
        if segments_rttm_list_union and segments_rttm_list_union[-1][1] >= begin - 0:
            segments_rttm_list_union[-1][1] = max(segments_rttm_list_union[-1][1], end)
        else:
            segments_rttm_list_union.append([begin, end])

    # print(segments_rttm_list_union)

    # details
    reference = Annotation()
    for i in segments_rttm_list_union:
        reference[Segment(i[0], i[1])] = 's'

    # print(reference)

    # print("-----------------------------------")
    hypothesis = Annotation()

    for i in segments_sec_union:
        hypothesis[Segment(i[0], i[1])] = 'S'
    # print(hypothesis)

    diarizationErrorRate = DiarizationErrorRate()
    result = diarizationErrorRate(reference, hypothesis, detailed=True, uem=Segment(0, 300))
    results.append((f"sample{audioNumber}", result))
    final_result['total'] += result['total']
    final_result['correct'] += result['correct']
    final_result['missed detection'] += result['missed detection']
    final_result['false alarm'] += result['false alarm']
    final_result['diarization error rate'] += result['diarization error rate']

final_result['diarization error rate'] = final_result['diarization error rate'] / sampleNumbers

for i in results:
    print(i)

print("final result : ", final_result)
