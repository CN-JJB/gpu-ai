(() => {
  const root = document.querySelector("[data-vram-budget]");
  if (!root) return;

  const q = name => root.querySelector(`[data-${name}]`);
  const inputs = ["params","bpw","layers","kvheads","headdim","kvbytes","context","concurrency","reserve","capacity"].map(q);
  const GiB = 1024 ** 3;

  function n(name) {
    return Math.max(0, Number(q(name).value) || 0);
  }

  function render() {
    const weights = n("params") * 1e9 * n("bpw") / 8 / GiB;
    const kv = 2 * n("layers") * n("kvheads") * n("headdim") * n("kvbytes") * n("context") * n("concurrency") / GiB;
    const reserve = n("reserve");
    const capacity = n("capacity");
    const total = weights + kv + reserve;
    const headroom = capacity - total;

    q("weights-out").textContent = weights.toFixed(2) + " GiB";
    q("kv-out").textContent = kv.toFixed(2) + " GiB";
    q("total-out").textContent = total.toFixed(2) + " GiB";
    q("headroom-out").textContent = headroom.toFixed(2) + " GiB";

    const denom = Math.max(capacity, total, 0.01);
    q("weights-bar").style.width = (weights / denom * 100) + "%";
    q("kv-bar").style.width = (kv / denom * 100) + "%";
    q("reserve-bar").style.width = (reserve / denom * 100) + "%";

    q("verdict").textContent = headroom < 0
      ? "纸面预算已经超过容量：先减少权重/KV/并发/context 或改变 offload 策略。"
      : "纸面上能放下，但这不是稳定运行保证；还要用真实 runtime telemetry 验证 allocator、workspace、offload 与峰值占用。";
  }

  inputs.forEach(el => el.addEventListener("input", render));
  render();
})();