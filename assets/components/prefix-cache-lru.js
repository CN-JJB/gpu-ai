(() => {
  const root = document.querySelector("[data-prefix-lru]");
  if (!root) return;
  const capInput = root.querySelector("[data-cache-capacity]");
  const capOut = root.querySelector("[data-cache-capacity-out]");
  const hitsOut = root.querySelector("[data-cache-hits]");
  const evictionsOut = root.querySelector("[data-cache-evictions]");
  const processedOut = root.querySelector("[data-prompt-processed]");
  const savedOut = root.querySelector("[data-prompt-saved]");
  const stepsRoot = root.querySelector("[data-cache-steps]");
  const sequence = ["A","B","A","C","A","B"];
  const prefix = 1024, suffix = 64;

  function render() {
    const capacity = Number(capInput.value);
    let cache = [];
    let hits = 0, evictions = 0, processed = 0, saved = 0;
    const steps = [];

    sequence.forEach(key => {
      const idx = cache.indexOf(key);
      const hit = idx >= 0 && capacity > 0;
      if (hit) {
        hits += 1;
        saved += prefix;
        processed += suffix;
        cache.splice(idx,1);
        cache.push(key);
      } else {
        processed += prefix + suffix;
        if (capacity > 0) {
          if (cache.length >= capacity) { cache.shift(); evictions += 1; }
          cache.push(key);
        }
      }
      steps.push({key, hit, cache:[...cache]});
    });

    capOut.textContent = String(capacity);
    hitsOut.textContent = String(hits);
    evictionsOut.textContent = String(evictions);
    processedOut.textContent = String(processed);
    savedOut.textContent = String(saved);

    stepsRoot.innerHTML = "";
    steps.forEach((s, i) => {
      const card = document.createElement("div");
      card.className = "cache-step";
      card.innerHTML = `<strong>#${i+1} · ${s.key} · ${s.hit ? "HIT" : "MISS"}</strong><span>cache: ${s.cache.length ? s.cache.join(" · ") : "empty"}</span>`;
      stepsRoot.appendChild(card);
    });
  }

  capInput.addEventListener("input", render);
  render();
})();