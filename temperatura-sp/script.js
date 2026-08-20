let state = { strike: '+0.0σ' };

function fmtRS(v) { return 'R$ ' + Number(v).toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); }
function fmtPct(v) { return (v * 100).toFixed(1).replace('.', ',') + '%'; }

function renderTicker() {
  const items = [];
  const janPremio = SITE_DATA.premiums['Janeiro']['+0.0σ'];
  items.push(`JANEIRO +0.0σ <b>${fmtRS(janPremio.premio)}</b>`);
  items.push(`SLOPE <b>${SITE_DATA.spec.slope} MW/PONTO</b>`);
  items.push(`${SITE_DATA.spec.totalContratos} CONTRATOS PRECIFICADOS`);
  items.push(`BASE <b>65°F / 18,33°C</b>`);
  items.push(`HISTÓRICO CLIMA <b>${SITE_DATA.spec.anosClimatologia}</b>`);
  items.push(`HISTÓRICO PLD <b>${SITE_DATA.spec.anosFinanceiro}</b>`);
  const html = items.join('&nbsp;&nbsp;·&nbsp;&nbsp;');
  document.getElementById('tickerTrack').innerHTML = html + '&nbsp;&nbsp;·&nbsp;&nbsp;' + html;
}

function renderHeroStats() {
  const stats = [
    [SITE_DATA.spec.totalContratos, 'Contratos precificados'],
    ['12', 'Meses (ano civil)'],
    ['45', 'Anos de temperatura'],
    ['CALL', 'Direção do payoff'],
  ];
  document.getElementById('heroStats').innerHTML = stats.map(([num, label]) => `
    <div class="stat"><div class="stat__num">${num}</div><div class="stat__label">${label}</div></div>
  `).join('');
}

function renderSpecTable() {
  const rows = [
    ['Instrumento', 'CALL sobre CDD'],
    ['Temperatura base', '65°F / 18,33°C'],
    ['Slope calibrado', `${SITE_DATA.spec.slope} MW/ponto CDD`],
    ['Localização', 'São Paulo (proxy SE/CO)'],
    ['Strikes', '±1,5σ da média (6 níveis)'],
    ['Desconto', 'Curva ETTJ (ANBIMA), diária'],
    ['Fonte de PLD', 'CCEE, semanal + diário 2021+'],
  ];
  document.getElementById('specTable').innerHTML = rows.map(([k, v]) => `
    <div class="spec__row"><span class="spec__k">${k}</span><span class="spec__v">${v}</span></div>
  `).join('');
}

function renderPills() {
  document.getElementById('strikePills').innerHTML = SITE_DATA.spec.strikes.map(s => `
    <button class="pill ${s === state.strike ? 'active' : ''}" data-strike="${s}">${s}</button>
  `).join('');
  document.querySelectorAll('[data-strike]').forEach(btn => {
    btn.addEventListener('click', () => { state.strike = btn.dataset.strike; update(); });
  });
}

function renderThermChain() {
  const meses = SITE_DATA.spec.meses;
  const maxCdd = Math.max(...meses.map(m => SITE_DATA.climatologia[m] || 0)) * 1.15;
  const abrev = { 'Janeiro':'JAN','Fevereiro':'FEV','Março':'MAR','Abril':'ABR','Maio':'MAI','Junho':'JUN',
                  'Julho':'JUL','Agosto':'AGO','Setembro':'SET','Outubro':'OUT','Novembro':'NOV','Dezembro':'DEZ' };

  const html = meses.map(mes => {
    const cdd = SITE_DATA.climatologia[mes] || 0;
    const dado = SITE_DATA.premiums[mes][state.strike];
    const fillPct = Math.min(100, (cdd / maxCdd) * 100);
    const strikePct = dado ? Math.min(100, (dado.strikeCdd / maxCdd) * 100) : 0;
    return `
      <div class="therm">
        <div class="therm__month">${abrev[mes]}</div>
        <div class="therm__tube">
          <div class="therm__fill" style="height:${fillPct}%"></div>
          <div class="therm__strike-line" style="bottom:${strikePct}%"></div>
        </div>
        <div class="therm__bulb"></div>
        <div class="therm__cdd">${cdd.toFixed(0)} CDD</div>
        <div class="therm__premio">${dado ? fmtRS(dado.premio) : '—'}</div>
        <div class="therm__prob">${dado ? fmtPct(dado.prob) : '—'}</div>
      </div>
    `;
  }).join('');
  document.getElementById('thermChain').innerHTML = html;
}

function renderClimaGrid() {
  const meses = SITE_DATA.spec.meses;
  const maxCdd = Math.max(...meses.map(m => SITE_DATA.climatologia[m] || 0));
  const abrev = { 'Janeiro':'JAN','Fevereiro':'FEV','Março':'MAR','Abril':'ABR','Maio':'MAI','Junho':'JUN',
                  'Julho':'JUL','Agosto':'AGO','Setembro':'SET','Outubro':'OUT','Novembro':'NOV','Dezembro':'DEZ' };
  document.getElementById('climaGrid').innerHTML = meses.map(mes => {
    const cdd = SITE_DATA.climatologia[mes] || 0;
    const h = Math.max(4, (cdd / maxCdd) * 100);
    return `
      <div class="clima-bar-wrap">
        <div class="clima-val">${cdd.toFixed(0)}</div>
        <div class="clima-bar" style="height:${h}%"></div>
        <div class="clima-month">${abrev[mes]}</div>
      </div>
    `;
  }).join('');
}

function renderRiskTables() {
  document.getElementById('basisRiskBody').innerHTML = SITE_DATA.basisRisk.map(r => `
    <tr>
      <td>${r.strike_desvios}</td>
      <td class="pos">${fmtPct(r.sensibilidade)}</td>
      <td>${fmtPct(r.precisao)}</td>
      <td class="neg">${fmtPct(r.taxa_falso_negativo)}</td>
    </tr>
  `).join('');
  document.getElementById('semiVarBody').innerHTML = SITE_DATA.semiVariancia.map(r => `
    <tr>
      <td>${r.strike_desvios}</td>
      <td>${fmtRS(r.premio_RS)}</td>
      <td class="pos">${r.efetividade_pct.toFixed(1).replace('.', ',')}%</td>
    </tr>
  `).join('');
}

const TIMELINE = [
  { pivot: false, title: 'Estrutura real do CME pesquisada, não inventada', desc: 'Fórmula exata de CDD, tick de US$20/ponto no mercado americano, e o achado que o CME nunca mistura cidades num índice — sempre uma estação por contrato.' },
  { pivot: true, title: 'Correlação direta CDD→PLD testada — e fraca', desc: 'r≈0,08-0,13, não significativa. PLD no Brasil é dominado por valor da água, não por demanda térmica — diferente do mercado americano onde o produto se inspira.' },
  { pivot: true, title: 'Tick fixo abandonado por bootstrap de pares reais', desc: 'Em vez de inventar um número em R$/ponto, o motor reamostra pares históricos (CDD,PLD) do mesmo mês — preserva a correlação fraca real, não assume uma mais forte.' },
  { pivot: false, title: 'Slope refinado: R² de 0,109 para 0,654', desc: 'Agregação mensal escondia o efeito de dia útil vs. fim de semana. Controlando por isso em nível diário, o modelo bateu a faixa da literatura internacional.' },
  { pivot: false, title: '65°F testado contra o clima de São Paulo', desc: 'Varredura de 14°C a 23,5°C no dado real — o ótimo empírico (18,5°C) ficou a 0,2°C da convenção americana. Coincidência explicável, não presumida.' },
  { pivot: true, title: 'Hedging effectiveness positiva — o oposto do agro', desc: 'Mesma metodologia (semi-variância) que deu resultado negativo no produto agrícola aqui deu 19,8% a 60,5% positivo — porque payoff e custo compartilham o mesmo PLD.' },
];

function renderTimeline() {
  document.getElementById('timeline').innerHTML = TIMELINE.map((t, i) => `
    <div class="tl-item ${t.pivot ? 'is-pivot' : ''}">
      <div class="tl-num">${String(i + 1).padStart(2, '0')}${t.pivot ? ' · PIVÔ' : ''}</div>
      <div class="tl-title">${t.title}</div>
      <div class="tl-desc">${t.desc}</div>
    </div>
  `).join('');
}

function update() {
  renderPills();
  renderThermChain();
}

renderTicker();
renderHeroStats();
renderSpecTable();
renderRiskTables();
renderTimeline();
renderClimaGrid();
update();
