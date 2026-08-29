(() => {
  const root=document.querySelector("[data-sampling-temp]");
  if(!root) return;
  const slider=root.querySelector("[data-temp]");
  const out=root.querySelector("[data-temp-out]");
  const bars=[...root.querySelectorAll("[data-prob]")];
  const logits=[4.2,3.4,2.8,1.7,0.9];
  function render(){
    const t=Math.max(0.05,Number(slider.value));
    const exps=logits.map(x=>Math.exp(x/t));
    const z=exps.reduce((a,b)=>a+b,0);
    const probs=exps.map(x=>x/z);
    out.textContent=t.toFixed(2);
    bars.forEach((el,i)=>{
      const p=probs[i];
      el.style.width=(p*100)+"%";
      el.textContent=(p*100).toFixed(1)+"%";
    });
  }
  slider.addEventListener("input",render);render();
})();