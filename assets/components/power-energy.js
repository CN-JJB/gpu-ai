(() => {
 const root=document.querySelector("[data-power-energy]"); if(!root) return;
 const q=n=>root.querySelector("[data-"+n+"]");
 function val(n){return Math.max(0,Number(q(n).value)||0);}
 function render(){
   const watts=val("watts"), tokps=Math.max(0.001,val("tokps")), tokens=val("tokens"), idle=val("idle");
   const time=tokens/tokps;
   const energy=watts*time;
   const jt=energy/Math.max(tokens,1);
   const net=Math.max(0,watts-idle);
   q("time-out").textContent=time.toFixed(2)+" s";
   q("energy-out").textContent=(energy/1000).toFixed(2)+" kJ";
   q("jpt-out").textContent=jt.toFixed(2)+" J/token";
   q("net-out").textContent=net.toFixed(0)+" W";
   q("note").textContent="J/token depends on both power and speed. A faster run can use higher watts yet lower total energy per token.";
 }
 ["watts","tokps","tokens","idle"].map(q).forEach(el=>el.addEventListener("input",render)); render();
})();