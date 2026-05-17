// Captain Cool — App Logic (Two-Screen: Command Center + War Room)

// ── Screen Navigation ─────────────────────────────────────
function goToWarRoom() {
  document.getElementById('screen-command').classList.add('hidden');
  document.getElementById('screen-command').classList.remove('screen-active');
  document.getElementById('screen-warroom').classList.remove('hidden');
  window.scrollTo(0, 0);
}

function goToCommandCenter() {
  document.getElementById('screen-warroom').classList.add('hidden');
  document.getElementById('screen-command').classList.remove('hidden');
  document.getElementById('screen-command').classList.add('screen-active');
  document.getElementById('submit-btn').disabled = false;
  document.getElementById('submit-text').textContent = 'Ask the Captain';
  window.scrollTo(0, 0);
}

// ── Captain Style Toggle ──────────────────────────────────
document.querySelectorAll('.captain-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.captain-btn').forEach(b => b.classList.remove('active-captain'));
    btn.classList.add('active-captain');
    document.getElementById('captain_style').value = btn.dataset.style;
  });
});

// ── Bowler Builder ────────────────────────────────────────
function addBowlerRow() {
  const list = document.getElementById('bowler-list');
  const row = document.createElement('div');
  row.className = 'bowler-row grid gap-2 items-center';
  row.style.gridTemplateColumns = '1fr 60px 32px';
  row.innerHTML = `
    <input type="text" class="form-ctrl bowler-name" placeholder="Bowler name" />
    <input type="number" class="form-ctrl bowler-overs text-center" value="1" min="1" max="4" />
    <button type="button" onclick="removeBowlerRow(this)" class="w-8 h-8 rounded-lg text-red-400 text-xs flex items-center justify-center" style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2)">✕</button>
  `;
  list.appendChild(row);
}

function removeBowlerRow(btn) {
  const rows = document.querySelectorAll('.bowler-row');
  if (rows.length <= 1) return;
  btn.closest('.bowler-row').remove();
}

// ── Build Payload ─────────────────────────────────────────
function buildPayload() {
  const bowlersRemaining = {};
  document.querySelectorAll('.bowler-row').forEach(row => {
    const name = row.querySelector('.bowler-name').value.trim();
    const overs = parseInt(row.querySelector('.bowler-overs').value) || 1;
    if (name) bowlersRemaining[name] = overs;
  });

  const bowlersUsed = {};
  Object.entries(bowlersRemaining).forEach(([n, rem]) => { bowlersUsed[n] = Math.max(0, 4 - rem); });

  return {
    innings: parseInt(document.getElementById('innings').value) || 2,
    over: parseInt(document.getElementById('over').value) || 16,
    ball: parseInt(document.getElementById('ball').value) || 0,
    current_score: parseInt(document.getElementById('current_score').value) || 145,
    wickets: parseInt(document.getElementById('wickets').value) || 3,
    target: parseInt(document.getElementById('target').value) || null,
    batting_team: document.getElementById('batting_team').value,
    bowling_team: document.getElementById('bowling_team').value,
    striker: document.getElementById('striker').value,
    striker_handedness: document.getElementById('striker_handedness').value,
    non_striker: document.getElementById('non_striker').value,
    bowlers_remaining: bowlersRemaining,
    bowlers_used: bowlersUsed,
    venue: document.getElementById('venue').value,
    pitch_type: document.getElementById('pitch_type').value,
    dew_factor: document.getElementById('dew_factor').checked ? 'Yes' : 'No',
    impact_player_available: document.getElementById('impact_player').checked,
    captain_style: document.getElementById('captain_style').value || 'Dhoni',
    phase: document.getElementById('phase').value,
  };
}

// ── Progress ──────────────────────────────────────────────
function advanceProgress(turn) {
  const pct = ((turn - 1) / 5) * 100;
  document.getElementById('progress-fill').style.width = pct + '%';
  for (let i = 1; i <= 5; i++) {
    const dot = document.getElementById(`dot-${i}`);
    dot.classList.remove('active', 'done');
    if (i < turn) dot.classList.add('done');
    else if (i === turn) dot.classList.add('active');
  }
}

function completeProgress() {
  document.getElementById('progress-fill').style.width = '100%';
  for (let i = 1; i <= 5; i++) {
    const dot = document.getElementById(`dot-${i}`);
    dot.classList.remove('active');
    dot.classList.add('done');
  }
}

// ── Typing Indicator ──────────────────────────────────────
function showTyping(emoji, name, message) {
  removeTyping();
  const el = document.createElement('div');
  el.className = 'typing-card';
  el.id = 'typing-indicator';
  el.innerHTML = `<span style="font-size:1.1rem">${emoji}</span><div class="typing-dots"><span></span><span></span><span></span></div><span style="font-size:12px;color:rgba(255,255,255,0.5)"><strong style="color:white">${name}</strong>: ${message}</span>`;
  document.getElementById('debate-transcript').appendChild(el);
  scrollDebate();
}

function removeTyping() {
  const el = document.getElementById('typing-indicator');
  if (el) el.remove();
}

function scrollDebate() {
  const t = document.getElementById('debate-transcript');
  t.scrollTop = t.scrollHeight;
}

// ── Render Agent Card ─────────────────────────────────────
function agentClass(name) {
  if (name.includes('Stats')) return 'card-stats';
  if (name.includes('Devil')) return 'card-devil';
  if (name.includes('Comment')) return 'card-commentator';
  return 'card-strategist';
}

function fmt(text) {
  return text
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')
    .replace(/^#{1,3} (.+)$/gm,'<strong style="color:#ffad4d">$1</strong>')
    .replace(/\n/g,'<br/>');
}

function renderCard(data) {
  removeTyping();
  const cls = agentClass(data.agent);
  const el = document.createElement('div');
  el.className = `agent-card ${cls}`;

  let toolHtml = '';
  if (data.tool_calls && data.tool_calls.length > 0) {
    const badges = data.tool_calls.map(t => `<span class="tool-badge">⚡ ${t.tool}</span>`).join('');
    toolHtml = `<div class="tool-calls-row">${badges}</div>`;
  }

  el.innerHTML = `
    <div class="agent-card-header">
      <span class="agent-card-emoji">${data.emoji}</span>
      <span class="agent-card-name">${data.agent}</span>
      <span class="agent-card-label">${data.label || ''}</span>
    </div>
    <div class="agent-card-body">${fmt(data.content || '')}</div>
    ${toolHtml}
  `;
  document.getElementById('debate-transcript').appendChild(el);
  scrollDebate();
}

// ── Context Bar ───────────────────────────────────────────
function updateContextBar(payload) {
  document.getElementById('ctx-teams').textContent = `${payload.batting_team} vs ${payload.bowling_team}`;
  document.getElementById('ctx-score').textContent = `${payload.current_score}/${payload.wickets}`;
  const rrr = payload.target ? (((payload.target - payload.current_score) / ((20 - payload.over) || 1)) * 1).toFixed(1) : '';
  document.getElementById('ctx-situation').textContent = `Over ${payload.over}.${payload.ball}${payload.target ? ` · RRR ${rrr}` : ''}`;
}

// ── SSE Debate ────────────────────────────────────────────
async function startDebate(payload) {
  goToWarRoom();
  updateContextBar(payload);

  document.getElementById('debate-transcript').innerHTML = '';
  document.getElementById('error-state').classList.add('hidden');
  document.getElementById('progress-fill').style.width = '0%';
  for (let i = 1; i <= 5; i++) { const d = document.getElementById(`dot-${i}`); d.classList.remove('active','done'); }
  document.getElementById('status-text').textContent = 'Starting...';

  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'text/event-stream' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      showError(err.detail || 'Server error. Check your GEMINI_API_KEY.');
      return;
    }

    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let buf = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop();
      let evtName = '', dataStr = '';
      for (const line of lines) {
        if (line.startsWith('event: ')) evtName = line.slice(7).trim();
        else if (line.startsWith('data: ')) dataStr = line.slice(6).trim();
        else if (line === '' && evtName && dataStr) {
          try { handleEvent(evtName, JSON.parse(dataStr)); } catch(e) {}
          evtName = ''; dataStr = '';
        }
      }
    }
  } catch(err) {
    showError(`Connection error: ${err.message}. Is the server running?`);
  }
}

function handleEvent(event, data) {
  switch(event) {
    case 'agent_start':
      advanceProgress(data.turn);
      document.getElementById('status-text').textContent = `Turn ${data.turn}/5`;
      showTyping(data.emoji, data.agent, data.message);
      break;
    case 'agent_done':
      renderCard(data);
      break;
    case 'complete':
      completeProgress();
      removeTyping();
      document.getElementById('status-text').textContent = 'Complete ✓';
      const banner = document.createElement('div');
      banner.className = 'final-banner';
      banner.innerHTML = '<p style="font-size:13px;font-weight:700;color:#ffd700">🏆 Captain has spoken. The call has been made.</p>';
      document.getElementById('debate-transcript').appendChild(banner);
      scrollDebate();
      break;
    case 'error':
      showError(data.message || 'An unknown error occurred.');
      break;
  }
}

function showError(msg) {
  removeTyping();
  document.getElementById('error-message').textContent = msg;
  document.getElementById('error-state').classList.remove('hidden');
  document.getElementById('status-text').textContent = 'Error';
}

// ── Form Submit ───────────────────────────────────────────
document.getElementById('match-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  document.getElementById('submit-btn').disabled = true;
  document.getElementById('submit-text').textContent = 'Starting debate...';
  const payload = buildPayload();
  await startDebate(payload);
});

// ── Health Check ──────────────────────────────────────────
async function checkHealth() {
  try {
    const res = await fetch('/api/health');
    const data = await res.json();
    if (!data.gemini_configured) {
      const warn = document.createElement('div');
      warn.className = 'api-warn';
      warn.innerHTML = '⚠️ <strong>GEMINI_API_KEY not set.</strong> Add it to <code>.env</code> in the project root — get yours at <a href="https://aistudio.google.com/apikey" target="_blank" style="color:#ff8a00">aistudio.google.com</a>.';
      document.querySelector('#screen-command header').after(warn);
    }
  } catch(e) {}
}
checkHealth();
