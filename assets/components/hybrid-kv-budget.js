(() => {
  const root=document.querySelector("[data-hybrid-kv]");
  if(!root) return;
  const q=n=>root.querySelector("[data-"+n+"]");
  const names=["fullLayers","localLayers","context","window"];
  function n(k){return Math.max(0,Number(q(k).value)||0);}
  function render(){
    const full=n("fullLayers"), local=n("localLayers"), ctx=n("context"), win=Math.min(ctx,n("window"));
    const allFull=(full+local)*ctx;
    const hybrid=full*ctx+local*win;
    const ratio=allFull>0?hybrid/allFull:0;
    q("factor-out").textContent=hybrid.toLocaleString();
    q("allfull-out").textContent=allFull.toLocaleString();
    q("ratio-out").textContent=(ratio*100).toFixed(1)+"%";
    q("saving-out").textContent=((1-ratio)*100).toFixed(1)+"%";
    q("verdict").textContent="在这个“每层每 token KV 成本相同”的教学模型里，hybrid attention 只保留全 full-attention baseline 的 "+(ratio*100).toFixed(1)+"%。真实模型还要按每层 KV heads/head_dim/cache policy 修正。";
  }
  names.map(q).forEach(el=>el.addEventListener("input",render));render();
})();