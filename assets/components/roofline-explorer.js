(() => {
  const root = document.querySelector("[data-roofline]");
  if (!root) return;

  const computeInput = root.querySelector("[data-compute]");
  const bandwidthInput = root.querySelector("[data-bandwidth]");
  const aiInput = root.querySelector("[data-ai]");
  const computeOut = root.querySelector("[data-compute-out]");
  const bandwidthOut = root.querySelector("[data-bandwidth-out]");
  const aiOut = root.querySelector("[data-ai-out]");
  const ridgeOut = root.querySelector("[data-ridge]");
  const perfOut = root.querySelector("[data-perf]");
  const boundOut = root.querySelector("[data-bound]");
  const memoryPath = root.querySelector("[data-memory-path]");
  const computePath = root.querySelector("[data-compute-path]");
  const point = root.querySelector("[data-roof-point]");
  const ridgeLine = root.querySelector("[data-ridge-line]");

  const x0 = 58, x1 = 610, y0 = 270, y1 = 30, aiMax = 120;

  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  const xForAI = ai => x0 + clamp(ai / aiMax, 0, 1) * (x1 - x0);

  function render() {
    const compute = Math.max(1, Number(computeInput.value));
    const bandwidth = Math.max(1, Number(bandwidthInput.value));
    const ai = Math.max(0.1, Number(aiInput.value));
    const ridge = compute * 1000 / bandwidth;
    const memoryRoof = bandwidth * ai / 1000;
    const perf = Math.min(compute, memoryRoof);
    const yForPerf = p => y0 - clamp(p / (compute * 1.15), 0, 1) * (y0 - y1);

    computeOut.textContent = compute.toFixed(1) + " TFLOP/s";
    bandwidthOut.textContent = bandwidth.toFixed(0) + " GB/s";
    aiOut.textContent = ai.toFixed(1) + " FLOP/B";
    ridgeOut.textContent = ridge.toFixed(1) + " FLOP/B";
    perfOut.textContent = perf.toFixed(2) + " TFLOP/s";
    boundOut.textContent = memoryRoof < compute ? "memory roof 更低 → bandwidth-bound 上限" : "compute roof 更低 → compute-bound 上限";

    const xr = xForAI(ridge);
    const yc = yForPerf(compute);
    memoryPath.setAttribute("d", `M ${x0} ${y0} L ${xr} ${yc}`);
    computePath.setAttribute("d", `M ${xr} ${yc} L ${x1} ${yc}`);
    ridgeLine.setAttribute("x1", xr);
    ridgeLine.setAttribute("x2", xr);
    ridgeLine.setAttribute("y1", yc);
    ridgeLine.setAttribute("y2", y0);
    point.setAttribute("cx", xForAI(ai));
    point.setAttribute("cy", yForPerf(perf));
  }

  [computeInput, bandwidthInput, aiInput].forEach(el => el.addEventListener("input", render));
  render();
})();