(() => {
 const root=document.querySelector("[data-little-law]"); if(!root) return;
 const q=n=>root.querySelector("[data-"+n+"]");
 function render(){
   const lambda=Math.max(0,Number(q("lambda").value)||0);
   const w=Math.max(0,Number(q("w").value)||0);
   const l=lambda*w;
   q("l-out").textContent=l.toFixed(2)+" requests";
   q("lambda-out").textContent=lambda.toFixed(2)+" req/s";
   q("w-out").textContent=w.toFixed(2)+" s";
   q("note").textContent="如果这里的 W 是“从 arrival 到 completion”，那么 L 代表 queue + active 的系统平均在途请求数；它不是 peak，也不给 p95。";
 }
 ["lambda","w"].map(q).forEach(el=>el.addEventListener("input",render)); render();
})();