#!/bin/bash
# ============================================================================
# substituir_excel.sh
# Acha a versao mais recente de "Derivativo_Precipitacao_Soja_MT*.xlsx" em
# ~/Downloads (cobre nomes como "_2", "_3", "(1)", ou dentro de subpastas
# numeradas que o navegador as vezes cria) e substitui o arquivo em
# ~/derivativo-soja, criando um backup com timestamp antes.
#
# USO:
#   chmod +x substituir_excel.sh   (so na primeira vez)
#   ./substituir_excel.sh
# ============================================================================
set -e

DOWNLOADS="$HOME/Downloads"
PASTA_PROJETO="$HOME/derivativo-soja"
DESTINO="$PASTA_PROJETO/Derivativo_Precipitacao_Soja_MT.xlsx"
CARIMBO=$(date +%Y%m%d_%H%M%S)
BACKUP="$PASTA_PROJETO/Derivativo_Precipitacao_Soja_MT_backup_${CARIMBO}.xlsx"

echo "Procurando o arquivo mais recente em $DOWNLOADS (ate 2 niveis de subpasta)..."

# -exec stat -f "%m %N" funciona no stat do macOS (BSD); %m = data de
# modificacao (epoch), %N = caminho. Ordena do mais recente pro mais antigo.
ARQUIVO=$(find "$DOWNLOADS" -maxdepth 2 -iname "Derivativo_Precipitacao_Soja_MT*.xlsx" \
    -exec stat -f "%m %N" {} \; 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

if [ -z "$ARQUIVO" ]; then
    echo "ERRO: nenhum arquivo 'Derivativo_Precipitacao_Soja_MT*.xlsx' encontrado em $DOWNLOADS"
    echo "Confirma se o download terminou antes de rodar este script de novo."
    exit 1
fi

echo "Encontrado: $ARQUIVO"
echo "  Modificado em: $(stat -f '%Sm' "$ARQUIVO")"
echo "  Tamanho: $(stat -f '%z' "$ARQUIVO") bytes"

if [ -f "$DESTINO" ]; then
    cp "$DESTINO" "$BACKUP"
    echo "Backup do arquivo atual criado: $BACKUP"
fi

mv "$ARQUIVO" "$DESTINO"
echo ""
echo "OK - substituido com sucesso:"
echo "  $DESTINO"
echo ""
echo "As automacoes (daily_update.py as 7h, atualizar_juros.py as 7h10) vao"
echo "usar esse arquivo normalmente amanha, sem precisar de mais nenhum passo."
