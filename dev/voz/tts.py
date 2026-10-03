"""Motor de voz: Lucía (piper sharvard, voz F), Pablo (piper davefx), Dora (kokoro ef_dora)."""
import sherpa_onnx, soundfile as sf, sys, subprocess, numpy as np
V='/tmp/voices/'
def make(kind):
    if kind=='kokoro':
        m=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
            model=V+'kokoro-multi-lang-v1_0/model.onnx',voices=V+'kokoro-multi-lang-v1_0/voices.bin',
            tokens=V+'kokoro-multi-lang-v1_0/tokens.txt',data_dir=V+'kokoro-multi-lang-v1_0/espeak-ng-data',
            lexicon=V+'kokoro-multi-lang-v1_0/lexicon-us-en.txt',lang='es'),num_threads=4)
    else:
        d=V+f'vits-piper-es_ES-{kind}-medium/'
        m=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
            model=d+f'es_ES-{kind}-medium.onnx',tokens=d+'tokens.txt',data_dir=d+'espeak-ng-data',
            length_scale=1.08,noise_scale=0.6,noise_scale_w=0.8),num_threads=4)
    return sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=m))
def say(tts,text,sid,out,speed=1.0):
    a=tts.generate(text,sid=sid,speed=speed)
    x=np.array(a.samples,dtype=np.float32)
    pad=np.zeros(int(a.sample_rate*0.15),dtype=np.float32)
    sf.write(out+'.wav',np.concatenate([pad,x,pad]),a.sample_rate)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',out+'.wav','-ac','1','-b:a','48k',out+'.mp3'],check=True)
    import os; os.remove(out+'.wav')
