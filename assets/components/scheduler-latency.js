(() => {
  const root = document.querySelector("[data-scheduler-sim]");
  if (!root) return;

  const slider = root.querySelector("[data-groups]");
  const groupText = root.querySelector("[data-group-count]");
  const utilText = root.querySelector("[data-issue-util]");
  const idleText = root.querySelector("[data-idle-cycles]");
  const traceRoot = root.querySelector("[data-schedule-trace]");
  const verdict = root.querySelector("[data-schedule-verdict]");

  function simulate(groupCount, cycles = 120) {
    const groups = Array.from({ length: groupCount }, () => ({ phase: 0, readyAt: 0 }));
    let rr = 0;
    let issued = 0;
    let idle = 0;
    const trace = [];

    for (let cycle = 0; cycle < cycles; cycle += 1) {
      let chosen = -1;
      for (let offset = 0; offset < groupCount; offset += 1) {
        const idx = (rr + offset) % groupCount;
        if (groups[idx].readyAt <= cycle) {
          chosen = idx;
          break;
        }
      }

      if (chosen === -1) {
        idle += 1;
        trace.push(-1);
        continue;
      }

      const g = groups[chosen];
      issued += 1;
      trace.push(chosen);

      if (g.phase === 4) {
        g.phase = 0;
        g.readyAt = cycle + 21;
      } else {
        g.phase += 1;
      }
      rr = (chosen + 1) % groupCount;
    }

    return { issued, idle, trace, utilization: issued / cycles };
  }

  function renderTrace(trace) {
    traceRoot.innerHTML = "";
    trace.slice(0, 72).forEach((group, cycle) => {
      const cell = document.createElement("span");
      cell.className = "cycle-cell " + (group < 0 ? "idle" : "issue");
      cell.title = group < 0 ? `cycle ${cycle}: scheduler idle` : `cycle ${cycle}: issue group ${group + 1}`;
      cell.textContent = group < 0 ? "·" : String((group % 9) + 1);
      traceRoot.appendChild(cell);
    });
  }

  function render() {
    const groups = Number(slider.value);
    const result = simulate(groups);
    groupText.textContent = String(groups);
    utilText.textContent = (result.utilization * 100).toFixed(1) + "%";
    idleText.textContent = String(result.idle);
    renderTrace(result.trace);

    if (result.utilization > 0.95) {
      verdict.textContent = "在这个教学模型里，ready groups 已基本覆盖 memory wait；继续加组的收益很小。";
    } else if (result.utilization > 0.65) {
      verdict.textContent = "更多 resident groups 正在把等待藏到其他工作后面，但 scheduler 仍有空洞。";
    } else {
      verdict.textContent = "可运行的组太少，一旦它们同时等待 memory，scheduler 就明显闲置。";
    }
  }

  slider.addEventListener("input", render);
  render();
})();