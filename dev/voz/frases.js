// Saca TODAS las frases que la app reproduce, con la misma lógica que src/app.html.
// Uso: node dev/voz/frases.js  -> JSON {clave: texto}
const fs = require("fs"), path = require("path");
const root = path.join(__dirname, "..", "..");
const app = fs.readFileSync(path.join(root, "src", "app.html"), "utf8");
const RETO = JSON.parse(fs.readFileSync(path.join(root, "dev", "dibujos", "reto.json"), "utf8"));
const grab = (start, end) => { const a = app.indexOf(start); const b = app.indexOf(end, a) + end.length; return app.slice(a, b); };
const NAME = "Ari";
eval(grab("const LESSONS = [", "\n];").replace("const LESSONS", "global.LESSONS"));
eval(grab("function introText(l){", "\n}\n").replace("function introText", "global.introText = function"));
eval(grab("function finText(l, already){", "\n}\n").replace("function finText", "global.finText = function"));
const out = { hola: "¡Hola, " + NAME + "! ¿Qué animal dibujamos hoy?" };
for (const l of [...LESSONS, ...RETO]) {
  l.steps.forEach((s, i) => { out[l.id + "-" + i] = s.say; });
  out[l.id + "-0i"] = introText(l) + l.steps[0].say;
  out[l.id + "-fin-nueva"] = finText(l, false);
  out[l.id + "-fin-otra"] = finText(l, true);
}
process.stdout.write(JSON.stringify(out));
