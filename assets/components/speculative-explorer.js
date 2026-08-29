(() => {
  const root = document.querySelector("[data-speculative]");
  if (!root) return;
  const pInput = root.querySelector("[data-acceptance]");
  const dInput = root.querySelector("[data-draft-length]");
  const pOut = root.querySelector("[data-acceptance-out]");
  const dOut = root.querySelector("[data-draft-length-out]");
  const progressOut = root.querySelector("[data-progress]");
  const costOut = root.querySelector("[data-spec-cost]");
  const speedOut = root.querySelector("[data-spec-speedup]");
  const chain = root.querySelector("[data-draft-chain]");
  const verdict = root.querySelector("[data-spec-verdict]");

  function render() {
    const p = Number(pInput.value);
    const d = Number(dInput.value);
    let accepted = 0;
    chain.innerHTML = "";
    for (let k=1; k<=d; k+=1) {
      const survive = p ** k;
      accepted += survive;
      const cell = document.createElement("span");
      cell.className = "draft-token";
      cell.innerHTML = `d${k}<small>${(survive*100).toFixed(1)}%</small>`;
      cell.title = `在简化独立模型里，走到 draft token ${k} 的概率约 ${(survive*100).toFixed(1)}%`;
      chain.appendChild(cell);
    }
    const progress = 1 + accepted;
    const cost = 1.08 + 0.12 * d;
    const speed = progress / cost;

    pOut.textContent = Math.round(p*100) + "%";
    dOut.textContent = String(d);
    progressOut.textContent = progress.toFixed(3) + " tokens/round";
    costOut.textContent = cost.toFixed(2) + " target-step units";
    speedOut.textContent = speed.toFixed(3) + "×";
    verdict.textContent = speed > 1
      ? "在这组抽象成本下有理论净收益；真实运行仍要比较 target-only 端到端 baseline。"
      : "在这组抽象成本下，proposal/verification 成本已经吃掉收益；更长 draft 不一定更好。";
  }

  [pInput,dInput].forEach(el => el.addEventListener("input",render));
  render();
})();