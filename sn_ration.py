with open('your_file.rttm') as f:
    lines = f.readlines()

start = 0
duration = 0
end = 0

noises = 0
s_speech = 0
m_speech = 0
durations = 0

for line in lines:

    start = float(line.split(' ')[3])
    duration = float(line.split(' ')[4])
    durations += duration
    if start >= end:
        s_speech += duration

    else:
        if (start+duration) <= end:
            if (start+duration) <= end_prev:
                pass
            else:
                s_speech -= duration + (start - max(start, end_prev))
                m_speech += duration - (start - max(start, end_prev))

        else:

            s_speech -= end - max(start, end_prev)
            m_speech += end - max(start, end_prev)
            s_speech += duration - (end - max(start, end_prev))

    end_prev = min(end, start + duration)
    end = max(end, start + duration)

noises = 3600 - s_speech - m_speech

print(noises / 3600)
print(s_speech / 3600)
print(m_speech / 3600)
print(noises + s_speech + m_speech)
print(durations)
