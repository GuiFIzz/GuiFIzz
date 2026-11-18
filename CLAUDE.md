# Regras deste repositório

## Regra permanente: chegou um relatório novo da usina

Vale para qualquer relatório mensal da comercializadora (hoje a Bro Energy). Definida pelo
usuário em 18/11/2026. Executar **todos** os cinco passos, nesta ordem, sem esperar ser pedido.

**1. Refazer os cálculos e atualizar a planilha.**
Salvar o PDF em `financeiro/relatorios/` com o padrão `AAAA_Mes.pdf` e rodar:

```bash
cd financeiro/scripts && python3 atualizar.py
```

Isso reconstrói a planilha inteira do zero a partir dos PDFs e recalcula as fórmulas.
Nunca editar a planilha à mão: ela é saída, não fonte. A fonte são os PDFs.
Se o recálculo acusar erro de fórmula, corrigir antes de entregar.

**2. Fazer qualquer análise que possa melhorar a condição da empresa.**
Não se limitar a atualizar números. Procurar ativamente: inadimplência nova, cliente perdido,
concentração, margem, tributo, cláusula contratual descumprida, dinheiro parado, custo evitável.
O que aparecer vira linha nas abas `Plano_de_Acao` e `Contas_a_Receber`.

**3. Se necessário, formular perguntas para a comercializadora.**
Toda pergunta tem que estar ancorada num número da planilha, nunca numa impressão.
Entram na aba `Perguntas_Bro`, com prioridade e com o efeito na decisão.
Se houver matéria suficiente, redigir o e-mail em `comunicacao/`.

**4. Análise completa de energia da usina.**
Produção, consumo, resultado do mês, estoque de créditos e **conciliação do saldo**:
a variação do saldo tem que bater com o resultado do mês. Diferença acima de 1.000 kWh é
crédito sumindo e precisa ser investigada e cobrada.
Conferir também os meses abaixo de 80% da produção média (referência operacional, não contratual).

**5. Reajustar o dashboard energético.**
A aba `Dashboard_Energia` se refaz sozinha no passo 1. Conferir se os gráficos e os KPIs
continuam coerentes e se o número de meses na série está certo.

Ao final, entregar a planilha ao usuário e resumir em texto o que mudou e o que ele precisa decidir.

## Contexto que não pode ser esquecido

- **O contrato GD-074-02-24 é de OUTRA empresa e não rege esta usina** (confirmado em 18/11/2026).
  A aba `Contrato_Bro` está suspensa e `empresas/.../01_Contrato_GD074_BroEnergy.md` está arquivado.
  Não citar cláusula, percentual, prazo ou multa daquele contrato com a Bro. O contrato correto
  será providenciado pelo sócio; quando chegar, refazer a aba a partir dele.
- A administração de 10% sobre o valor pago e a taxa de 50% do primeiro faturamento de cliente novo
  **estão corretas e acordadas** — confirmado pelo sócio. Não questionar.
- FOTOVOLT CURRAL NOVO SPE é a dona do ativo; LF AGROPASTORIL recebe o repasse.
  Não misturar com Agropastoril dos Poções. Ver `empresas/Fotovolt_Curral_Novo/`.
- Contato na comercializadora: **Luana, da Bro Energy**.
- A planilha é `financeiro/LF_Agropastoril_Analise_Relatorios_2026.xlsx`.
- O conhecimento das empresas fica em `empresas/`, em markdown, no formato Entity Overview.
- Dinheiro sempre conferido contra o rodapé do PDF de origem. Nunca digitar número à mão.
- Números estimados (tributos, produtividade de kWp) ficam em célula azul, editável,
  e são sempre marcados como estimativa a confirmar com o contador.
