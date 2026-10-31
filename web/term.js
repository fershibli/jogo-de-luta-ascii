// Main thread: xterm.js terminal + keyboard ring buffer shared with the Python worker.
(async () => {
  if (!window.crossOriginIsolated) {
    if (!('serviceWorker' in navigator)) { document.getElementById('status').textContent = 'Navegador sem suporte a Service Worker.'; return; }
    const reg = await navigator.serviceWorker.register('coi-sw.js');
    if (!sessionStorage.getItem('coi-reloaded')) {
      sessionStorage.setItem('coi-reloaded', '1');
      await navigator.serviceWorker.ready;
      location.reload();
      return;
    }
    document.getElementById('status').textContent = 'Não consegui ativar o isolamento (SharedArrayBuffer). Tente recarregar.';
    return;
  }
  sessionStorage.removeItem('coi-reloaded');
  const cfg = window.GAME || {};
  const term = new Terminal({
    cols: cfg.cols || 80, rows: cfg.rows || 30, convertEol: true, cursorBlink: true,
    fontFamily: '"Cascadia Mono", Consolas, "Lucida Console", monospace', fontSize: 15,
    theme: { background: '#000000', foreground: '#c0c0c0', cursor: '#c0c0c0' },
  });
  term.open(document.getElementById('term'));
  term.focus();

  const N = 8192;
  const sab = new SharedArrayBuffer(16 + N);
  const hdr = new Int32Array(sab, 0, 4);
  const data = new Uint8Array(sab, 16, N);
  const enc = new TextEncoder();
  const push = (s) => {
    for (const b of enc.encode(s)) {
      const w = Atomics.load(hdr, 0);
      data[w % N] = b;
      Atomics.store(hdr, 0, w + 1);
    }
    Atomics.notify(hdr, 0);
    bump();
  };
  // hdr[2] counts every event (key or network message), so the worker can wait for either.
  const bump = () => { Atomics.add(hdr, 2, 1); Atomics.notify(hdr, 2); };
  term.onData(push);

  // ---- network: the games' UDP sockets travel over WebRTC (PeerJS) ----
  const NN = 1 << 16;
  const netSab = new SharedArrayBuffer(16 + NN);
  const nhdr = new Int32Array(netSab, 0, 4);
  const ndata = new Uint8Array(netSab, 16, NN);
  const netPush = (obj) => {
    const bytes = enc.encode(JSON.stringify(obj));
    let w = Atomics.load(nhdr, 0);
    const frame = [bytes.length & 255, bytes.length >> 8, ...bytes];
    for (const b of frame) { ndata[w % NN] = b; w++; }
    Atomics.store(nhdr, 0, w);
    bump();
  };
  const PREFIX = 'fershibli-retro-' + (cfg.net || 'game') + '-';
  let peer = null;
  const conns = {}, queued = {};
  const loadPeer = () => new Promise((ok, fail) => {
    if (window.Peer) return ok();
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/peerjs@1.5.4/dist/peerjs.min.js';
    s.crossOrigin = 'anonymous';
    s.onload = ok; s.onerror = fail;
    document.head.appendChild(s);
  });
  const wire = (c) => {
    const code = c.peer.slice(PREFIX.length);
    conns[code] = c;
    c.on('open', () => {
      for (const d of queued[code] || []) c.send(d);
      delete queued[code];
      status.textContent = 'Conectado com a sala ' + code + '.';
    });
    c.on('data', (d) => netPush({ t: 'pkt', f: code, d }));
    c.on('close', () => { delete conns[code]; status.textContent = 'A conexão com ' + code + ' caiu.'; });
    c.on('error', (e) => { status.textContent = 'Erro de conexão: ' + e; });
  };
  const openPeer = async () => {
    if (peer) return;
    status.textContent = 'Abrindo uma sala no servidor...';
    try { await loadPeer(); } catch (e) { netPush({ t: 'err', m: 'não consegui carregar o PeerJS' }); return; }
    const tryOpen = () => {
      const code = String(1000 + Math.floor(Math.random() * 9000));
      peer = new Peer(PREFIX + code);
      peer.on('open', () => { status.textContent = 'Sua sala: ' + code + ' (passe esse número no lugar do IP).'; netPush({ t: 'id', code }); });
      peer.on('connection', wire);
      peer.on('error', (e) => {
        if (e.type === 'unavailable-id') { peer.destroy(); tryOpen(); }
        else if (e.type === 'peer-unavailable') status.textContent = 'Essa sala não existe (ainda). Confira o número.';
        else status.textContent = 'Rede: ' + e.type;
      });
    };
    tryOpen();
  };
  const netSend = (to, d) => {
    if (!peer) return;
    to = String(to).trim();
    let c = conns[to];
    if (!c) { c = peer.connect(PREFIX + to, { reliable: true, serialization: 'json' }); wire(c); }
    if (c.open) c.send(d); else (queued[to] = queued[to] || []).push(d);
  };

  const status = document.getElementById('status');
  const worker = new Worker('worker.js');
  worker.onmessage = (e) => {
    const m = e.data;
    if (m.t === 'out') term.write(m.s);
    else if (m.t === 'status') status.textContent = m.s;
    else if (m.t === 'title') document.title = m.s;
    else if (m.t === 'net-open') openPeer();
    else if (m.t === 'net-send') netSend(m.to, m.d);
  };
  worker.postMessage({ t: 'start', sab, netSab, game: cfg, base: location.href.replace(/[^/]*$/, '') });
  document.getElementById('term').addEventListener('click', () => term.focus());
})();
