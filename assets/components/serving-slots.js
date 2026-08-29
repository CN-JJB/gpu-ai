(() => {
  const root = document.querySelector("[data-serving-slots]");
  if (!root) return;
  const slotsInput = root.querySelector("[data-slots]");
  const slotsOut = root.querySelector("[data-slots-out]");
  const modeInput = root.querySelector("[data-mode]");
  const makespanOut = root.querySelector("[data-makespan]");
  const waitOut = root.querySelector("[data-first-wait]");
  const timeline = root.querySelector("[data-request-timelines]");
  const note = root.querySelector("[data-serving-note]");

  const requests = [
    {id:"A", arrival:0, work:6},{id:"B", arrival:0, work:2},{id:"C", arrival:0, work:7},{id:"D", arrival:0, work:3},
    {id:"E", arrival:1, work:4},{id:"F", arrival:2, work:2},{id:"G", arrival:3, work:6},{id:"H", arrival:4, work:3}
  ];

  function simulateContinuous(slotCount) {
    const state = requests.map(r => ({...r, remaining:r.work, start:null, end:null, states:[]}));
    let active = [];
    let t = 0;
    while (state.some(r => r.end === null) && t < 60) {
      const ready = state.filter(r => r.arrival <= t && r.start === null);
      while (active.length < slotCount && ready.length) {
        const r = ready.shift(); r.start = t; active.push(r);
      }
      for (const r of state) {
        if (t < r.arrival || r.end !== null) r.states[t] = "off";
        else if (active.includes(r)) r.states[t] = "active";
        else r.states[t] = "queue";
      }
      active.forEach(r => r.remaining -= 1);
      const done = active.filter(r => r.remaining <= 0);
      done.forEach(r => r.end = t + 1);
      active = active.filter(r => r.remaining > 0);
      t += 1;
    }
    return state;
  }

  function simulateStatic(slotCount) {
    const state = requests.map(r => ({...r, remaining:r.work, start:null, end:null, states:[]}));
    let batch = [];
    let t = 0;
    while (state.some(r => r.end === null) && t < 80) {
      if (batch.length === 0) {
        batch = state.filter(r => r.arrival <= t && r.start === null).slice(0, slotCount);
        batch.forEach(r => r.start = t);
      }
      for (const r of state) {
        if (t < r.arrival || r.end !== null) r.states[t] = "off";
        else if (batch.includes(r)) r.states[t] = "active";
        else r.states[t] = "queue";
      }
      batch.forEach(r => r.remaining -= 1);
      if (batch.length && batch.every(r => r.remaining <= 0)) {
        batch.forEach(r => r.end = t + 1);
        batch = [];
      }
      t += 1;
    }
    return state;
  }

  function renderRows(state) {
    const maxT = Math.max(...state.map(r => r.end || 0));
    timeline.innerHTML = "";
    state.forEach(r => {
      const row = document.createElement("div");
      row.className = "request-row";
      const label = document.createElement("span");
      label.className = "request-label";
      label.textContent = r.id;
      row.appendChild(label);
      for (let t=0; t<maxT; t+=1) {
        const cell = document.createElement("span");
        const s = r.states[t] || "off";
        cell.className = "request-tick " + s;
        cell.title = `request ${r.id}, t=${t}: ${s}`;
        cell.textContent = s === "active" ? "■" : (s === "queue" ? "·" : "");
        row.appendChild(cell);
      }
      timeline.appendChild(row);
    });
  }

  function render() {
    const slots = Number(slotsInput.value);
    const mode = modeInput.value;
    const state = mode === "continuous" ? simulateContinuous(slots) : simulateStatic(slots);
    const makespan = Math.max(...state.map(r => r.end || 0));
    const avgWait = state.reduce((s,r)=>s + ((r.start ?? r.arrival) - r.arrival),0) / state.length;
    slotsOut.textContent = String(slots);
    makespanOut.textContent = makespan + " time units";
    waitOut.textContent = avgWait.toFixed(2) + " units";
    renderRows(state);
    note.textContent = mode === "continuous"
      ? "Continuous：请求一结束就立刻补入空 slot，短请求能更早释放容量。"
      : "Static：这一批必须全部结束才开启下一批；短请求结束后的空位会浪费。";
  }

  [slotsInput, modeInput].forEach(el => el.addEventListener("input", render));
  render();
})();