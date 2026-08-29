(() => {
  const root = document.querySelector("[data-quant-bpw]");
  if (!root) return;
  const q = name => root.querySelector(`[data-${name}]`);
  const inputs = ["codebits","groupsize","scalebits","highfrac","highbits","params"].map(q);

  function n(name) { return Math.max(0, Number(q(name).value) || 0); }

  function render() {
    const codeBits = n("codebits");
    const groupSize = Math.max(1, n("groupsize"));
    const scaleBits = n("scalebits");
    const highFrac = Math.min(1, n("highfrac") / 100);
    const highBits = n("highbits");
    const paramsB = n("params");

    const lowBpw = codeBits + scaleBits / groupSize;
    const wholeBpw = (1 - highFrac) * lowBpw + highFrac * highBits;
    const gib = paramsB * 1e9 * wholeBpw / 8 / (1024 ** 3);

    q("low-out").textContent = lowBpw.toFixed(3) + " bpw";
    q("whole-out").textContent = wholeBpw.toFixed(3) + " bpw";
    q("gib-out").textContent = gib.toFixed(2) + " GiB";
    q("highfrac-out").textContent = (highFrac * 100).toFixed(0) + "%";

    const overhead = lowBpw - codeBits;
    q("explain").textContent =
      `低-bit 区域：${codeBits.toFixed(1)} code bits + ${overhead.toFixed(3)} scale bits/weight；再与 ${(highFrac*100).toFixed(0)}% 的高精度 tensor 混合。`;
  }

  inputs.forEach(el => el.addEventListener("input", render));
  render();
})();