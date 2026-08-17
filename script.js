// ============================================================================
// ESTADO
// ============================================================================
let state = {
  city: SITE_DATA.spec.cidades[0],
  strike: '50%',
};

const MESES_ABREV = {
  'Setembro': 'SET', 'Outubro': 'OUT', 'Novembro': 'NOV',
  'Dezembro': 'DEZ', 'Janeiro': 'JAN', 'Fevereiro': 'FEV',
};
const MESES_CRITICOS = ['Janeiro', 'Fevereiro'];

function fmtRS(v) {
  return 'R$ ' + Number(v).toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
}
function fmtPct(v) {
  return (v * 100).toFixed(1).replace('.', ',') + '%';
}

// ============================================================================
// TICKER
// ============================================================================
function renderTicker() {
  const items = [];
  SITE_DATA.spec.cidades.forEach(cidade => {
    const jan = SITE_DATA.premiums[cidade]['Janeiro']['50%'];
    items.push(`${cidade.toUpperCase()} JAN 50% <b>${fmtRS(jan.premio)}</b>`);
  });
  items.push(`SAFRA ATIVA <b>${SITE_DATA.spec.safraAtiva}</b>`);
  items.push(`${SITE_DATA.spec.totalContratos} CONTRATOS PRECIFICADOS`);
  items.push(`HISTÓRICO <b>${SITE_DATA.spec.anosHistorico}</b>`);
  items.push(`TICK <b>R$ ${SITE_DATA.spec.tick}/mm</b>`);
  items.push(`CAP <b>${SITE_DATA.spec.cap}mm</b>`);
  const html = items.join('&nbsp;&nbsp;·&nbsp;&nbsp;');
  document.getElementById('tickerTrack').innerHTML = html + '&nbsp;&nbsp;·&nbsp;&nbsp;' + html;
}

// ============================================================================
// HERO STATS
// ============================================================================
function renderHeroStats() {
  const stats = [
    [SITE_DATA.spec.totalContratos, 'Contratos precificados'],
    ['3', 'Municípios · MT'],
    ['36', 'Anos de histórico'],
    [SITE_DATA.spec.safraAtiva, 'Safra ativa'],
  ];
  document.getElementById('heroStats').innerHTML = stats.map(([num, label]) => `
    <div class="stat">
      <div class="stat__num">${num}</div>
      <div class="stat__label">${label}</div>
    </div>
  `).join('');
}

// ============================================================================
// SPEC TABLE
// ============================================================================
function renderSpecTable() {
  const rows = [
    ['Instrumento', 'PUT sobre chuva'],
    ['Tick', `R$ ${SITE_DATA.spec.tick}/mm`],
    ['Cap', `${SITE_DATA.spec.cap}mm/mês`],
    ['Payoff máx.', fmtRS(SITE_DATA.spec.cap * SITE_DATA.spec.tick) + '/contrato'],
    ['Carga de risco', fmtPct(SITE_DATA.spec.cargaRisco)],
    ['Liquidação', 'Financeira, D+dias'],
    ['Desconto', 'Curva ETTJ (ANBIMA), diária'],
  ];
  document.getElementById('specTable').innerHTML = rows.map(([k, v]) => `
    <div class="spec__row"><span class="spec__k">${k}</span><span class="spec__v">${v}</span></div>
  `).join('');
}

// ============================================================================
// PILLS (cidade / strike)
// ============================================================================
function renderPills() {
  document.getElementById('cityPills').innerHTML = SITE_DATA.spec.cidades.map(c => `
    <button class="pill ${c === state.city ? 'active' : ''}" data-city="${c}">${c}</button>
  `).join('');
  document.getElementById('strikePills').innerHTML = SITE_DATA.spec.strikes.map(s => `
    <button class="pill ${s === state.strike ? 'active' : ''}" data-strike="${s}">${s}</button>
  `).join('');

  document.querySelectorAll('[data-city]').forEach(btn => {
    btn.addEventListener('click', () => { state.city = btn.dataset.city; update(); });
  });
  document.querySelectorAll('[data-strike]').forEach(btn => {
    btn.addEventListener('click', () => { state.strike = btn.dataset.strike; update(); });
  });
}

// ============================================================================
// RAIN GAUGE CHAIN (elemento assinatura)
// ============================================================================
function renderGaugeChain() {
  const meses = SITE_DATA.spec.meses;
  const cityClima = SITE_DATA.climatologia[state.city];
  const maxMm = Math.max(...meses.map(m => cityClima[m] || 0)) * 1.15;

  const html = meses.map(mes => {
    const mm = cityClima[mes] || 0;
    const dado = SITE_DATA.premiums[state.city][mes][state.strike];
    const fillPct = Math.min(100, (mm / maxMm) * 100);
    const strikePct = dado ? Math.min(100, (dado.strikeMm / maxMm) * 100) : 0;
    const critico = MESES_CRITICOS.includes(mes);

    return `
      <div class="gauge ${critico ? 'gauge--critical' : ''}">
        <div class="gauge__month">${MESES_ABREV[mes]}${critico ? ' ★' : ''}</div>
        <div class="gauge__tube">
          <div class="gauge__fill" style="height:${fillPct}%"></div>
          <div class="gauge__strike-line" style="bottom:${strikePct}%"></div>
        </div>
        <div class="gauge__mm">${mm.toFixed(0)}mm méd.</div>
        <div class="gauge__premio">${dado ? fmtRS(dado.premio) : '—'}</div>
        <div class="gauge__prob">${dado ? fmtPct(dado.prob) : '—'} acion.</div>
      </div>
    `;
  }).join('');

  document.getElementById('gaugeChain').innerHTML = html;
}

// ============================================================================
// CLIMATOLOGY BARS
// ============================================================================
function renderClimaGrid() {
  const meses = SITE_DATA.spec.meses;
  const cityClima = SITE_DATA.climatologia[state.city];
  const maxMm = Math.max(...meses.map(m => cityClima[m] || 0));

  document.getElementById('climaGrid').innerHTML = meses.map(mes => {
    const mm = cityClima[mes] || 0;
    const h = Math.max(4, (mm / maxMm) * 100);
    return `
      <div class="clima-bar-wrap">
        <div class="clima-val">${mm.toFixed(0)}</div>
        <div class="clima-bar" style="height:${h}%"></div>
        <div class="clima-month">${MESES_ABREV[mes]}</div>
      </div>
    `;
  }).join('');
}

// ============================================================================
// BASIS RISK / SEMI-VARIANCE TABLES
// ============================================================================
function renderRiskTables() {
  document.getElementById('basisRiskBody').innerHTML = SITE_DATA.basisRisk.map(r => `
    <tr>
      <td>${r.strike}</td>
      <td class="pos">${fmtPct(r.sensibilidade)}</td>
      <td>${fmtPct(r.precisao)}</td>
      <td class="neg">${fmtPct(r.taxa_falso_negativo)}</td>
    </tr>
  `).join('');

  document.getElementById('semiVarBody').innerHTML = SITE_DATA.semiVariancia.map(r => `
    <tr>
      <td>${r.strike}</td>
      <td class="neg">${r.efetividade_critico_pct.toFixed(1).replace('.', ',')}%</td>
      <td class="neg">${r.efetividade_temporada_pct.toFixed(1).replace('.', ',')}%</td>
      <td>${r.custo_premio_critico_pct_payoff_max.toFixed(1).replace('.', ',')}%</td>
    </tr>
  `).join('');
}

// ============================================================================
// TIMELINE
// ============================================================================
const TIMELINE = [
  { pivot: false, title: 'Hipótese inicial: índice de produtividade', desc: 'Regressão de clima contra produtividade detrendada, buscando um índice que precificasse uma opção sobre safra.' },
  { pivot: true, title: 'Overfitting exposto por validação cruzada', desc: 'R² in-sample de 0,26 caiu para 0,07 fora da amostra (LOYO) — o sinal era em grande parte artefato de grid search, não relação real.' },
  { pivot: false, title: 'Motor reconstruído com literatura, não busca', desc: 'Parâmetros bioclimáticos ancorados em papers (estresse térmico, Curve Number por solo), Curve Number por cidade — overfitting reduzido, mas R² permaneceu baixo.' },
  { pivot: true, title: 'Pivô: de índice de produtividade a paramétrico puro', desc: 'Em vez de apostar numa relação clima→produtividade fraca, o produto passou a pagar direto sobre o índice de chuva — como a CME realmente estrutura esses contratos.' },
  { pivot: false, title: 'Motor CME-style: HBA + Monte Carlo + curva de juros real', desc: 'Cadeia de 108 contratos, curva ETTJ da ANBIMA (não uma taxa única), safra rolante, automação diária local via launchd.' },
  { pivot: true, title: 'Basis risk quantificado — não só mencionado', desc: 'Matriz de acerto/erro e, na metodologia padrão da literatura (semi-variância), a efetividade do hedge saiu negativa no tamanho ingênuo de contrato — um limite honesto, não escondido.' },
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

// ============================================================================
// UPDATE / INIT
// ============================================================================
function update() {
  renderPills();
  renderGaugeChain();
  renderClimaGrid();
}

renderTicker();
renderHeroStats();
renderSpecTable();
renderRiskTables();
renderTimeline();
update();
