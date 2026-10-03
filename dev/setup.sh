#!/usr/bin/env bash
# Prepara una sesión nueva. Uso:
#   bash dev/setup.sh        -> dependencias para dibujos, build y test
#   bash dev/setup.sh voz    -> además descarga los 3 modelos de voz (~500 MB, solo si hay que grabar frases)
set -e
pip install -q --break-system-packages shapely svgpathtools pillow playwright sherpa-onnx soundfile 2>/dev/null || true
python3 -c "import playwright" && (python3 -m playwright install chromium >/dev/null 2>&1 || true)
if [ "$1" = "voz" ]; then
  mkdir -p /tmp/voices && cd /tmp/voices
  base=https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models
  for m in vits-piper-es_ES-sharvard-medium vits-piper-es_ES-davefx-medium kokoro-multi-lang-v1_0; do
    [ -d "$m" ] || { curl -sSL -o "$m.tar.bz2" "$base/$m.tar.bz2" && tar xjf "$m.tar.bz2" && rm "$m.tar.bz2"; }
  done
  echo "Modelos de voz listos en /tmp/voices"
fi
echo "Setup OK"
