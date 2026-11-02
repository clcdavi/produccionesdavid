const ptIds = ["gancho", "logo", "napo", "rucula", "roquefort", "emp1", "r1", "r2", "r3", "resena", "cierre"];
ptIds.forEach((id, idx) => {
  const p = P[id];
  const s0 = idx % 2 === 0 ? 1.13 : 1.03;
  const s1 = idx % 2 === 0 ? 1.03 : 1.13;
  tl.fromTo(`#cam-${id}`, { scale: s0 }, { scale: s1, duration: p.dur, ease: "none" }, p.ini);
});

// Crossfades
tl.fromTo("#plano-napo",   { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "sine.inOut" }, P.napo.ini - 0.35);
tl.fromTo("#plano-resena", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "sine.inOut" }, P.resena.ini - 0.35);
tl.fromTo("#plano-cierre", { opacity: 0 }, { opacity: 1, duration: 0.40, ease: "sine.inOut" }, P.cierre.ini - 0.40);

// Top badge
tl.fromTo("#top-ticket", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }, P.napo.ini);

// 1. GANCHO
tl.fromTo("#pt-g-tag", { opacity: 0, scale: 1.3, rotation: -3 }, { opacity: 1, scale: 1, rotation: -1, duration: 0.35, ease: "back.out(1.8)" }, P.gancho.ini + 0.08);
tl.fromTo("#pt-g-tit .w", { opacity: 0, y: 45 }, { opacity: 1, y: 0, duration: 0.4, stagger: 0.07, ease: "power3.out" }, P.gancho.ini + 0.22);

// 2. LOGO
tl.fromTo("#pt-flash", { opacity: 0.92 }, { opacity: 0, duration: 0.38, ease: "power2.out" }, P.logo.ini);
tl.fromTo("#pt-logo-box", { opacity: 0, scale: 1.4, rotation: -4 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.7)" }, P.logo.ini);
tl.fromTo("#pt-logo-sub", { opacity: 0, y: 35 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, P.logo.ini + PULSO);

// 3-6. PIZZAS & EMPANADAS
function animarCaja(cardSel, titSel, subSel, tIni) {
  tl.fromTo(cardSel, { opacity: 0, y: 65, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.38, ease: "back.out(1.5)" }, tIni);
  tl.fromTo(`${titSel} .l`, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, stagger: 0.015, ease: "power2.out" }, tIni + 0.1);
  tl.fromTo(subSel, { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, tIni + 0.32);
}

animarCaja("#card-napo",   "#tit-napo",   "#sub-napo",   P.napo.ini);
animarCaja("#card-rucula", "#tit-rucula", "#sub-rucula", P.rucula.ini);
animarCaja("#card-roq",    "#tit-roq",    "#sub-roq",    P.roquefort.ini);
animarCaja("#card-emp",    "#tit-emp",    "#sub-emp",    P.emp1.ini);

// 7-9. RAFAGA
tl.fromTo("#pop-r1", { opacity: 0, scale: 1.35, rotation: -3 }, { opacity: 1, scale: 1, rotation: -1, duration: 0.32, ease: "back.out(1.8)" }, P.r1.ini);
tl.fromTo("#pop-r2", { opacity: 0, scale: 1.35, rotation: 3 },  { opacity: 1, scale: 1, rotation: 1,  duration: 0.32, ease: "back.out(1.8)" }, P.r2.ini);
tl.fromTo("#pop-r3", { opacity: 0, scale: 1.35, rotation: -2 }, { opacity: 1, scale: 1, rotation: 0,  duration: 0.32, ease: "back.out(1.8)" }, P.r3.ini);

// 10. RESENA
tl.fromTo("#pt-res-card", { opacity: 0, y: 55, rotation: -1 }, { opacity: 1, y: 0, rotation: 0, duration: 0.45, ease: "back.out(1.5)" }, P.resena.ini);
tl.fromTo("#pt-res-quote .w", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.28, stagger: 0.032, ease: "power2.out" }, P.resena.ini + 0.2);
tl.fromTo("#pt-res-badge", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, P.resena.ini + PULSO * 2);

// 11. CIERRE
tl.fromTo("#pt-cierre-box",  { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, P.cierre.ini);
tl.fromTo("#pt-cierre-logo", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.7)" }, P.cierre.ini + 0.15);
tl.fromTo("#pt-cta",         { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, P.cierre.ini + 0.3);
tl.fromTo("#pt-info .pt-info-item", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.35, stagger: 0.12, ease: "power2.out" }, P.cierre.ini + 0.45);
