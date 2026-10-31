// Worker: runs the original game with Pyodide; stdin/time.sleep block for real via Atomics.
importScripts('https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js');
let hdr, data, N, sleeper, nhdr, ndata, NN;
const post = (t, s) => postMessage({ t, s });
const avail = () => Atomics.load(hdr, 0) - Atomics.load(hdr, 1);
function readbyte(timeout) {
  while (avail() <= 0) {
    const w = Atomics.load(hdr, 0);
    const r = Atomics.wait(hdr, 0, w, timeout < 0 ? Infinity : timeout);
    if (r === 'timed-out' && avail() <= 0) return -1;
  }
  const rd = Atomics.load(hdr, 1);
  const b = data[rd % N];
  Atomics.store(hdr, 1, rd + 1);
  return b;
}
function sleep(ms) { if (ms > 0) Atomics.wait(sleeper, 0, 0, ms); }
// events: hdr[2] is bumped on every key and network message
const evseq = () => Atomics.load(hdr, 2);
function waitev(seq, ms) { if (ms > 0) Atomics.wait(hdr, 2, seq, ms); }
const dec = new TextDecoder();
function netrecv() {
  // next network message as JSON text, or '' when there is none
  const w = Atomics.load(nhdr, 0);
  let r = Atomics.load(nhdr, 1);
  if (w - r < 2) return '';
  const len = ndata[r % NN] | (ndata[(r + 1) % NN] << 8);
  const out = new Uint8Array(len);
  for (let i = 0; i < len; i++) out[i] = ndata[(r + 2 + i) % NN];
  Atomics.store(nhdr, 1, r + 2 + len);
  return dec.decode(out);
}

onmessage = async (e) => {
  const m = e.data;
  if (m.t !== 'start') return;
  const sab = m.sab;
  hdr = new Int32Array(sab, 0, 4);
  N = sab.byteLength - 16;
  data = new Uint8Array(sab, 16, N);
  sleeper = new Int32Array(new SharedArrayBuffer(4));
  NN = m.netSab.byteLength - 16;
  nhdr = new Int32Array(m.netSab, 0, 4);
  ndata = new Uint8Array(m.netSab, 16, NN);
  post('status', 'Carregando o Python (Pyodide)...');
  const py = await loadPyodide();
  py.registerJsModule('webterm', {
    write: (s) => post('out', s),
    readbyte, avail, sleep, evseq, waitev, netrecv,
    netopen: () => postMessage({ t: 'net-open' }),
    netsend: (to, d) => postMessage({ t: 'net-send', to, d }),
    title: (s) => post('title', s),
  });
  post('status', 'Carregando o jogo...');
  const files = await (await fetch(m.base + 'manifest.json')).json();
  py.FS.mkdirTree('/game');
  for (const f of files) {
    const buf = new Uint8Array(await (await fetch(m.base + 'game/' + f.split('/').map(encodeURIComponent).join('/'))).arrayBuffer());
    const dir = '/game/' + f.split('/').slice(0, -1).join('/');
    if (dir !== '/game/') py.FS.mkdirTree(dir);
    py.FS.writeFile('/game/' + f, buf);
  }
  py.FS.writeFile('/home/pyodide/webrt.py', await (await fetch(m.base + 'webrt.py')).text());
  py.FS.writeFile('/home/pyodide/msvcrt.py', await (await fetch(m.base + 'msvcrt.py')).text());
  for (const f of ['green.py', 'netsock.py'])
    py.FS.writeFile('/home/pyodide/' + f, await (await fetch(m.base + f)).text());
  post('status', 'Rodando. Clique no terminal para digitar.');
  try {
    py.runPython(`import sys; sys.path.insert(0, '/home/pyodide'); import webrt; webrt.run(${JSON.stringify(m.game.main)})`);
  } catch (err) {
    post('out', '\r\n\x1b[31m' + String(err).replace(/\n/g, '\r\n') + '\x1b[0m\r\n');
  }
  post('status', 'Fim. Recarregue a página para jogar de novo.');
};
