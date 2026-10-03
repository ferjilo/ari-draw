"""Graba con las 3 voces las frases que falten en audio/<voz>/<clave>.mp3.
Uso: python3 dev/voz/gen_audio.py            -> solo las que faltan
     python3 dev/voz/gen_audio.py gato-r-3   -> fuerza regrabar esas claves (si cambiaste el texto)
Requiere: bash dev/setup.sh voz"""
import json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, "..", ".."))
sys.path.insert(0, here)
from tts import make, say
frases = json.loads(subprocess.run(["node", os.path.join(here, "frases.js")], capture_output=True, text=True, check=True).stdout)
force = set(sys.argv[1:])
CFG = {"lucia": ("sharvard", 1, 1.0), "pablo": ("davefx", 0, 1.0), "dora": ("kokoro", 28, 0.92)}
for vid, (kind, sid, speed) in CFG.items():
    d = os.path.join(root, "audio", vid); os.makedirs(d, exist_ok=True)
    todo = [k for k in frases if k in force or not os.path.exists(os.path.join(d, k + ".mp3"))]
    if not todo: print(vid, "nada que grabar"); continue
    tts = make(kind)
    for k in todo: say(tts, frases[k], sid, os.path.join(d, k), speed)
    print(vid, "grabadas", len(todo))
