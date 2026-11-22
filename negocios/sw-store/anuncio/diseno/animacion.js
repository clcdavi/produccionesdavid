const swIds = ["gancho", "logo", "kraft", "interior", "tamanos", "personalizados", "cierre"];

// Subtle extra dynamic zoom punch on each video cut
swIds.forEach((id, idx) => {
  const p = P[id];
  const s0 = idx % 2 === 0 ? 1.05 : 1.0;
  const s1 = idx % 2 === 0 ? 1.0 : 1.05;
  tl.fromTo(`#cam-${id}`, { scale: s0 }, { scale: s1, duration: p.dur, ease: "none" }, p.ini);
});

// Quick punchy crossfades
tl.fromTo("#plano-kraft",   { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.out" }, P.kraft.ini - 0.2);
tl.fromTo("#plano-tamanos", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.out" }, P.tamanos.ini - 0.2);
tl.fromTo("#plano-cierre",  { opacity: 0 }, { opacity: 1, duration: 0.25, ease: "power2.out" }, P.cierre.ini - 0.25);

// Persistent top tag
tl.fromTo("#top-tag", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.28, ease: "back.out(1.6)" }, P.kraft.ini);

// 1. GANCHO
tl.fromTo("#sw-g-tag", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(1.8)" }, P.gancho.ini + 0.05);
tl.fromTo("#sw-g-tit .w", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, stagger: 0.04, ease: "power3.out" }, P.gancho.ini + 0.14);

// 2. LOGO
tl.fromTo("#sw-flash", { opacity: 0.85 }, { opacity: 0, duration: 0.28, ease: "power2.out" }, P.logo.ini);
tl.fromTo("#sw-logo-box", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.7)" }, P.logo.ini);
tl.fromTo("#sw-logo-lema", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, P.logo.ini + 0.22);

// 3-6. PRODUCT LOWER THIRDS
function animarCard(cardSel, titSel, subSel, tIni) {
  tl.fromTo(cardSel, { opacity: 0, y: 40, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.28, ease: "back.out(1.5)" }, tIni);
  tl.fromTo(`${titSel} .l`, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.22, stagger: 0.01, ease: "power2.out" }, tIni + 0.06);
  tl.fromTo(subSel, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.25, ease: "power2.out" }, tIni + 0.2);
}

animarCard("#card-kraft",          "#tit-kraft",          "#sub-kraft",          P.kraft.ini);
animarCard("#card-interior",       "#tit-interior",       "#sub-interior",       P.interior.ini);
animarCard("#card-tamanos",        "#tit-tamanos",        "#sub-tamanos",        P.tamanos.ini);
animarCard("#card-personalizados", "#tit-personalizados", "#sub-personalizados", P.personalizados.ini);

// 7. CIERRE
tl.fromTo("#sw-cierre-box",   { opacity: 0, y: 35, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.5)" }, P.cierre.ini);
tl.fromTo("#sw-cierre-logo",  { opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.7)" }, P.cierre.ini + 0.12);
tl.fromTo("#sw-cierre-frase", { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, P.cierre.ini + 0.25);
tl.fromTo("#sw-cierre-datos", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, P.cierre.ini + 0.38);
tl.fromTo("#sw-cierre-cta",   { opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, P.cierre.ini + 0.52);
