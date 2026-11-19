import sys,json
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[2],device="cpu",compute_type="int8")
import soundfile as sf; a,_=sf.read(sys.argv[1],dtype="float32"); segs,_=m.transcribe(a,language="th",word_timestamps=True,beam_size=5)
out=[]
for s in segs:
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}")
    for w in s.words: out.append([round(w.start,2),round(w.end,2),w.word])
json.dump(out,open(sys.argv[3],"w"),ensure_ascii=False)
for w in out: print(w)
