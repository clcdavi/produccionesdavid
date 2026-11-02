// Camera movements for every shot (gives life to real photos)
const ids = ["gancho", "logo", "salon", "parrilla", "asado", "achuras", "mila", "r1", "r2", "resena", "cierre"];
ids.forEach((id, idx) => {
  const p = P[id];
  const s0 = idx % 2 === 0 ? 1.14 : 1.04;
  const s1 = idx % 2 === 0 ? 1.04 : 1.14;
  tl.fromTo(`#cam-${id}`, { scale: s0 }, { scale: s1, duration: p.dur, ease: "none" }, p.ini);
});

// Crossfade transitions for shots that have "antes"
tl.fromTo("#plano-salon",    { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "sine.inOut" }, P.salon.ini - 0.35);
tl.fromTo("#plano-parrilla", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "sine.inOut" }, P.parrilla.ini - 0.35);
tl.fromTo("#plano-resena",   { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "sine.inOut" }, P.resena.ini - 0.35);
tl.fromTo("#plano-cierre",   { opacity: 0 }, { opacity: 1, duration: 0.40, ease: "sine.inOut" }, P.cierre.ini - 0.40);

// Persistent header pill
tl.fromTo("#cabecera-fija", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, P.salon.ini);

// 1. GANCHO
tl.fromTo("#g-tag", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, P.gancho.ini + 0.1);
tl.fromTo("#g-tit .w", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, stagger: 0.08, ease: "power3.out" }, P.gancho.ini + 0.25);

// 2. LOGO (Beat drop!)
tl.fromTo("#destello-logo", { opacity: 0.9 }, { opacity: 0, duration: 0.4, ease: "power2.out" }, P.logo.ini);
tl.fromTo("#logo-caja", { opacity: 0, scale: 1.35 }, { opacity: 1, scale: 1, duration: 0.45, ease: "expo.out" }, P.logo.ini);
tl.fromTo("#logo-sub", { opacity: 0, y: 35 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.6)" }, P.logo.ini + PULSO);

// 3. SALON
tl.fromTo("#s-pil", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, P.salon.ini + 0.1);
tl.fromTo("#s-tit .w", { opacity: 0, y: 36 }, { opacity: 1, y: 0, duration: 0.4, stagger: 0.07, ease: "power3.out" }, P.salon.ini + 0.2);

// 4-7. DISH CARDS
function animarPlato(cardSel, titSel, descSel, tIni) {
  tl.fromTo(cardSel, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, tIni);
  tl.fromTo(`${titSel} .l`, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.35, stagger: 0.018, ease: "power2.out" }, tIni + 0.1);
  tl.fromTo(descSel, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, tIni + 0.35);
}

animarPlato("#p-card",  "#p-tit",  "#p-desc",  P.parrilla.ini);
animarPlato("#a-card",  "#a-tit",  "#a-desc",  P.asado.ini);
animarPlato("#ac-card", "#ac-tit", "#ac-desc", P.achuras.ini);
animarPlato("#m-card",  "#m-tit",  "#m-desc",  P.mila.ini);

// 8-9. RAPID BEATS (R1, R2)
tl.fromTo("#r1-sello", { opacity: 0, scale: 1.3, rotation: -3 }, { opacity: 1, scale: 1, rotation: -1, duration: 0.3, ease: "back.out(1.8)" }, P.r1.ini);
tl.fromTo("#r2-sello", { opacity: 0, scale: 1.3, rotation: 3 },  { opacity: 1, scale: 1, rotation: 1,  duration: 0.3, ease: "back.out(1.8)" }, P.r2.ini);

// 10. RESENA
tl.fromTo("#res-card", { opacity: 0, y: 50, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "power3.out" }, P.resena.ini);
tl.fromTo("#res-cita .w", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.3, stagger: 0.035, ease: "power2.out" }, P.resena.ini + 0.2);
tl.fromTo("#res-efec", { opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.7)" }, P.resena.ini + PULSO * 2);

// 11. CIERRE
tl.fromTo("#c-panel", { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, P.cierre.ini);
tl.fromTo("#c-logo",  { opacity: 0, scale: 1.18 }, { opacity: 1, scale: 1, duration: 0.45, ease: "expo.out" }, P.cierre.ini + 0.15);
tl.fromTo("#c-cta",   { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, P.cierre.ini + 0.3);
tl.fromTo("#c-datos .dato-fila", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.35, stagger: 0.12, ease: "power2.out" }, P.cierre.ini + 0.45);
