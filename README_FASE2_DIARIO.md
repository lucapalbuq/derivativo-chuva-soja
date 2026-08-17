# Fase 2 — Atualização Diária de Chuva e Repricing Contínuo

Este README explica como rodar `daily_update.py` localmente via Claude Code
(ou qualquer Python 3 local), agendado por `cron`, para manter o preço da
PUT do mês ativo atualizado com a chuva realizada dia a dia.

## Por que rodar localmente, não no chat

O ambiente de chat do Claude tem acesso de rede restrito e não consegue
chamar a API do NASA POWER (explicado em detalhe na conversa). Rodando
localmente (Claude Code, terminal, ou qualquer máquina com Python e
internet normal), essa mesma chamada funciona sem bloqueio.

## 1. Instalação

```bash
# no diretório onde estão os arquivos do projeto:
pip3 install requests pandas numpy scipy openpyxl
```

Arquivos necessários na mesma pasta:
- `cme_structurer_v2.py`, `curva_juros.py`, `safra.py` (motor já existente)
- `chuva_previsao.py`, `nasa_power_fetch.py`, `daily_update.py` (novos, Fase 2)
- `Derivativo_Precipitacao_Soja_MT.xlsx` (a planilha a ser atualizada)
- `uploads/` com os 3 CSVs do histórico NASA POWER (`POWER_NASA_Sorriso.csv`,
  `POWER_NASA_Sinop.csv`, `POWER_NASA_Lucas_Do_RV.csv`) — usados como semente
  de ~35 anos de histórico (1990–hoje). **Sem essa pasta o repricing não
  funciona**: `daily_update.py` mistura esse histórico com o cache diário da
  API (`clima_cache/`, criado automaticamente) a cada execução, porque a API
  só retorna alguns dias por chamada — sozinha ela nunca teria anos
  suficientes para o HBA/Monte Carlo. `BASE`/`UPLOADS` em
  `cme_structurer_v2.py` apontam para a pasta do projeto (`Path(__file__).parent`),
  não mais para os caminhos do sandbox (`/home/claude/...`, `/mnt/user-data/...`)
  da sessão original do chat.

## 2. Testar manualmente antes de agendar

```bash
python3 daily_update.py                      # roda para hoje
python3 daily_update.py --data 2026-01-15    # roda para uma data especifica (reprocessar)
```

Se a data escolhida não cair dentro de um mês de contrato (Set–Fev), o
script avisa e não faz nada — isso é esperado, não é erro.

## 3. Agendamento (roda sozinho, todo dia)

**Não usa `crontab`**: neste Mac, editar o crontab do usuário dá erro de
permissão do macOS (`Operation not permitted`, restrição de TCC sobre
automação/Full Disk Access). Em vez disso, o agendamento é feito via
**launchd** (o mecanismo nativo do macOS, funciona sem essa restrição),
com um LaunchAgent em
`~/Library/LaunchAgents/com.derivativosoja.dailyupdate.plist`, rodando
todo dia às **7h** (antes da atualização da curva de juros às 8h — não há
dependência entre as duas, é só para manter os horários organizados).

Importante: `python3` do sistema (`/usr/bin/python3`) **não tem** as libs
instaladas (pandas, numpy, etc.) — o LaunchAgent usa o Python do Anaconda
(`/opt/anaconda3/bin/python3`, onde `pip3 install` da seção 1 instalou as
dependências). Se o Python "certo" mudar de lugar no futuro (reinstalação
do Anaconda, etc.), atualize o caminho no `.plist`.

Comandos úteis:
```bash
# ver se está carregado
launchctl list | grep derivativosoja

# disparar uma execução manual agora, sem esperar as 7h (útil para testar)
launchctl start com.derivativosoja.dailyupdate

# ver o log da última execução
tail -f logs/daily_update.log

# desativar (ex: para pausar a automação)
launchctl unload ~/Library/LaunchAgents/com.derivativosoja.dailyupdate.plist

# reativar
launchctl load ~/Library/LaunchAgents/com.derivativosoja.dailyupdate.plist
```

Limitação do launchd (igual valeria para cron): só roda se a sessão do
usuário estiver ativa (Mac ligado e logado) no horário agendado. Se o Mac
estiver desligado/dormindo às 7h, aquele dia não roda — não há
"catch-up" automático depois. Vale conferir de vez em quando (`tail -f
logs/daily_update.log`) se está rodando todo dia mesmo.

## 4. O que o script faz, resumido

1. Busca a chuva dos últimos dias (NASA POWER) para as 3 cidades.
2. Identifica a safra e o mês de contrato ativos (regra Março–Fevereiro).
3. Se hoje está dentro de um mês de contrato: projeta a chuva do mês
   inteiro (realizada até hoje + simulação dos dias restantes) e
   reprecifica esse contrato (HBA + Monte Carlo, mesmas funções do motor
   original).
4. Grava um log histórico (`monitor_diario_log.csv`) e atualiza a tabela
   "Monitor Diário" na aba **Próximas Fases** do Excel.
5. Contratos de meses futuros (ainda não iniciados) não são tocados.

## 5. Metodologia da projeção — e suas limitações (leia antes de confiar no número)

**Como funciona**: para os dias que faltam no mês, o script olha o que
choveu nos MESMOS dias restantes em cada ano histórico (ex: se hoje é
15/jan, olha 16–31/jan de cada ano do histórico) e usa essa distribuição
como cenário de "chuva possível daqui até o fim do mês". Isso é chamado de
previsão climatológica — não usa nenhum modelo meteorológico numérico, só
o padrão histórico do calendário.

**Validação que fizemos**: rodamos esse método retroativamente em 8
combinações aleatórias de mês/ano/dia com dado real já conhecido. Em 6 de
8 casos (75%), o valor real ficou dentro do intervalo P10–P90 projetado —
próximo do esperado (80%) para esse tipo de intervalo, com amostra pequena.
Em um caso (janeiro/2020, Sorriso), o mês real foi mais seco que qualquer
cenário do intervalo — evidência de que o método **não captura secas
anômalas fora do padrão histórico**.

**O que isso significa na prática**: use o número do dia como uma
estimativa de ordem de grandeza, atualizada e melhor que "só a
climatologia pura sem nenhum dado do mês corrente" — mas não como uma
previsão meteorológica de precisão. Para reduzir esse gap, o próximo passo
natural é combinar esse método com uma previsão meteorológica de curto
prazo (7–14 dias) para os dias mais próximos, e só usar o climatológico
para os dias mais distantes — não implementado nesta fase.

## 6. Troubleshooting

- **Erro 403 da API do NASA POWER**: só deve acontecer se você rodar de um
  ambiente com rede restrita (como o sandbox do chat). Rodando do seu Mac
  normalmente, não deve ocorrer.
- **"Chuva do dia" às vezes reflete um dia de 2-3 dias atrás, não "ontem"**:
  não é bug — é a defasagem real de consolidação do NASA POWER, medida em
  produção: o dia D-1 (e às vezes D-2) frequentemente vêm nulos na API,
  só D-3 costuma vir preenchido. `_chuva_do_dia()` em `daily_update.py` já
  procura para trás pelo dia mais recente com dado consolidado (janela de
  7 dias) em vez de assumir "ontem" fixo. O cache (`clima_cache/`) se
  autocorrige nos dias seguintes, conforme a API consolida os dados.
- **"Cabeçalho Data não encontrado"**: a aba Próximas Fases do Excel foi
  editada manualmente e a tabela Monitor Diário mudou de lugar/nome — ajuste
  `atualizar_excel_monitor()` em `daily_update.py` ou restaure a aba original.
- **Excel não abre / parece corrompido**: rode
  `python3 /caminho/para/recalc.py arquivo.xlsx` (script de validação usado
  neste projeto) antes de abrir, para confirmar que não há erro de fórmula.
