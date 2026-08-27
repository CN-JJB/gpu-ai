(() => {
  const root = document.querySelector("[data-pipeline-sim]");
  if (!root) return;
  const slider = root.querySelector("input[type=range]");
  const vertexText = root.querySelector("[data-vertex]");
  const pixelText = root.querySelector("[data-pixel]");
  const fixedUtil = root.querySelector("[data-fixed-util]");
  const unifiedUtil = root.querySelector("[data-unified-util]");
  const fixedBar = root.querySelector("[data-fixed-bar]");
  const unifiedBar = root.querySelector("[data-unified-bar]");
  const verdict = root.querySelector("[data-verdict]");

  function render() {
    const v = Number(slider.value) / 100;
    const p = 1 - v;
    const fixedTime = Math.max(v / 0.5, p / 0.5);
    const fUtil = 1 / fixedTime;
    const uUtil = 1 / 1.05;
    const unifiedTime = 1.05;

    vertexText.textContent = Math.round(v * 100) + "%";
    pixelText.textContent = Math.round(p * 100) + "%";
    fixedUtil.textContent = Math.round(fUtil * 100) + "%";
    unifiedUtil.textContent = Math.round(uUtil * 100) + "%";
    fixedBar.style.width = (fUtil * 100) + "%";
    unifiedBar.style.width = (uUtil * 100) + "%";

    const speedup = fixedTime / unifiedTime;
    verdict.textContent = speedup > 1
      ? "这个 workload 下，统一池概念模型约快 " + speedup.toFixed(2) + "×。"
      : "这个 workload 正好适配固定分区；统一池的 5% 抽象开销让它略慢。";
  }
  slider.addEventListener("input", render);
  render();
})();
