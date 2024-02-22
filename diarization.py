from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token="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")
diarization = pipeline("audio.wav/home/aibox/workstation/afshin/pyannot_v2/own_file/Sony1Labs/test/audio/023_30_M.mp3")
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
