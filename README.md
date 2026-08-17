# Derivativo Paramétrico de Precipitação — Soja MT

Derivativo climático estilo CME/CBOT para hedge de risco de precipitação da soja no
Médio-Norte de Mato Grosso (Sorriso, Sinop, Lucas do Rio Verde). Estruturação,
precificação (HBA + Monte Carlo), curva de juros real (ANBIMA), automação diária local,
e quantificação honesta do basis risk (matriz de acerto/erro + semi-variância,
metodologia Vedenov & Barnett 2004).

**[→ Ver a página interativa](https://SEU-USUARIO.github.io/NOME-DO-REPO/)** (ajuste este
link depois de publicar — veja o passo 3 abaixo)

## Estrutura deste repositório

```
├── index.html          # página principal (estática, sem build step)
├── style.css           # sistema de design
├── script.js           # interatividade (cadeia de strikes, tabelas)
├── data.js             # snapshot dos dados calculados (embutido, não dinâmico)
├── Memorial_Tecnico_Derivativo_Chuva_Soja.docx
├── Derivativo_Precipitacao_Soja_MT.xlsx
├── cme_structurer_v2.py       # motor de precificação (HBA + Monte Carlo)
├── curva_juros.py             # curva ETTJ (ANBIMA)
├── safra.py                   # modelo de safra rolante
├── daily_update.py            # automação diária de chuva
├── atualizar_juros.py         # automação diária de juros
├── chuva_previsao.py          # projeção de chuva do mês ativo
├── nasa_power_fetch.py        # busca de dados NASA POWER
├── basis_risk_analysis.py     # matriz de acerto/erro
├── semi_variancia_analysis.py # hedging effectiveness (Vedenov-Barnett)
└── README.md
```

## Como publicar no GitHub Pages

1. **Criar o repositório**: no GitHub, "New repository" → dá um nome (ex:
   `derivativo-chuva-soja`) → público (necessário para GitHub Pages gratuito) → criar
   vazio, sem README (você já tem um).

2. **Subir os arquivos**: pela interface web (arraste todos os arquivos desta pasta na
   página do repositório) ou via terminal:
   ```
   git init
   git add .
   git commit -m "Derivativo paramétrico de chuva - soja MT"
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/NOME-DO-REPO.git
   git push -u origin main
   ```

3. **Ativar o GitHub Pages**: no repositório, vá em **Settings → Pages**. Em "Source",
   selecione **Deploy from a branch**, branch **main**, pasta **/ (root)**. Salve.
   Leva 1-2 minutos para publicar. O link fica em
   `https://SEU-USUARIO.github.io/NOME-DO-REPO/`.

4. **Atualizar o link no README e no currículo** com a URL real gerada no passo 3.

## Sobre os dados da página (`data.js`)

A página é **estática** — os números vêm de um snapshot (`data.js`) gerado a partir dos
CSVs de resultado do motor de precificação, não de uma conexão ao vivo com a automação
local (`daily_update.py`/`atualizar_juros.py`, que rodam no seu Mac via `launchd`).

Para atualizar o snapshot manualmente depois de rodar o motor de novo:
```python
import json
# ... carregar strip_precificacao_v2.csv, historico_chuva_mensal_v2.csv,
#     basis_risk_matriz_confusao.csv, semi_variancia_resultado.csv como antes,
#     e reescrever site/data.js
```
(O script usado para gerar o `data.js` atual está documentado no memorial técnico,
Seção 12 — pode ser adaptado para rodar automaticamente via GitHub Actions como próximo
passo, mantendo a página sempre com o dado mais recente sem precisar fazer isso à mão.)

## Metodologia (resumo)

- **Precificação**: Historical Burn Analysis + Monte Carlo (distribuição Gamma, modelo
  hurdle para meses secos), 50.000 simulações por contrato.
- **Desconto**: curva de juros futura real (ETTJ ANBIMA), não uma taxa única — cada
  contrato descontado pela taxa do seu próprio vencimento.
- **Basis risk**: quantificado por matriz de acerto/erro e por redução de
  semi-variância (Vedenov & Barnett, 2004) — a métrica padrão da literatura acadêmica
  de weather derivatives, não uma métrica inventada para este projeto.
- **Detalhes completos, incluindo o que não funcionou e por quê**: ver o memorial
  técnico neste repositório.

## Stack

Python (pandas, numpy, scipy, openpyxl, statsmodels) para o motor de precificação e
análise; HTML/CSS/JS puro (sem framework, sem build step) para a página.
