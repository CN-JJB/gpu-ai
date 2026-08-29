(() => {
  const root=document.querySelector("[data-rope-explorer]");
  if(!root) return;
  const p=root.querySelector("[data-rope-position]");
  const freq=root.querySelector("[data-rope-frequency]");
  const pOut=root.querySelector("[data-rope-position-out]");
  const fOut=root.querySelector("[data-rope-frequency-out]");
  const angleOut=root.querySelector("[data-rope-angle]");
  const line=root.querySelector("[data-rope-vector]");
  const tip=root.querySelector("[data-rope-tip]");
  const cx=150, cy=150, r=95;
  function render(){
    const pos=Number(p.value), f=Number(freq.value);
    const angle=pos*f;
    const x=cx+r*Math.cos(angle), y=cy-r*Math.sin(angle);
    pOut.textContent=String(pos);
    fOut.textContent=f.toFixed(3);
    angleOut.textContent=(angle%(Math.PI*2)).toFixed(2)+" rad";
    line.setAttribute("x2",x);line.setAttribute("y2",y);
    tip.setAttribute("cx",x);tip.setAttribute("cy",y);
  }
  [p,freq].forEach(el=>el.addEventListener("input",render));render();
})();