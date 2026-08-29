(() => {
  const root=document.querySelector("[data-max-buy]");
  if(!root) return;
  const q=n=>root.querySelector(`[data-${n}]`);
  const names=["budget","upgrades","maintenance","risk","transaction","watch"];
  function val(n){return Math.max(0,Number(q(n).value)||0);}
  function render(){
    const ceiling=val("budget")-val("upgrades")-val("maintenance")-val("risk")-val("transaction");
    const watchUpper=ceiling+val("watch");
    q("ceiling-out").textContent=ceiling.toFixed(0);
    q("watch-out").textContent=watchUpper.toFixed(0);
    q("reserve-out").textContent=(val("upgrades")+val("maintenance")+val("risk")+val("transaction")).toFixed(0);
    q("verdict").textContent=ceiling<0
      ?"系统/TCO 成本已经超过总项目预算：当前候选没有正的 sticker ceiling。"
      :"这个数字只是 personal ceiling，不是 BUY signal；condition/support/performance gate 仍需通过。";
  }
  names.map(q).forEach(el=>el.addEventListener("input",render));render();
})();