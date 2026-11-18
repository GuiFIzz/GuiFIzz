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

## Regra permanente: chegou um extrato bancário novo

Salvar o PDF em `financeiro/extratos/` e rodar:

```bash
cd financeiro/scripts && python3 atualizar_consolidado.py
```

Reconstrói a planilha consolidada do zero a partir dos relatórios de energia e dos extratos.
O saldo final da aba Extrato tem que bater com o saldo do extrato do banco — conferir sempre.
Depois: procurar categoria nova (um fornecedor que nunca apareceu é um fato novo),
distribuição feita com caixa curto, imposto fora do padrão e operação entre partes relacionadas.

## Regra permanente: as planilhas vivem em DOIS lugares

O GitHub é a oficina (fontes, scripts, regras). O Google Drive é a vitrine (onde sócios e
contador abrem). Toda vez que uma planilha for reconstruída, publicar nos dois.

Passo extra depois de rodar `atualizar.py` ou `atualizar_consolidado.py`:
substituir o arquivo correspondente na pasta do Drive, pelos IDs abaixo.

```
Pasta no Drive : 1hG4wic6wDg0EmmedjfSTZ_p-KJKkUAcQ
  Consolidado  : 1SQY7LGd19iPWHTBqogaLH2VTfG4OQphr
  Operacional  : 16WMK23mSJRujMVJZsuJHJgMvX-RvPg0B
  LEIA-ME      : 1p2uk8Slfbp5_j8QK2e9bJgJETZe5Y4etrteMnzgkGfM
```

Subir sempre com `disableConversionToGoogleType: true`, para o arquivo continuar .xlsx e
não perder fórmulas nem gráficos na conversão para Google Sheets.
Se o LEIA-ME da pasta estiver desatualizado quanto à base de dados, atualizar também.

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
- Entradas vindas da **SPE POÇÕES LOCAÇÃO DE EQUIPAMENTOS** são **estorno de imposto pago pela
  empresa errada** (mesmo diretor nas duas), não receita. Classificar sempre como redução de
  imposto na categoria `Estorno de Imposto (SPE Poções)`.
- São DUAS planilhas, com papéis diferentes:
  `financeiro/Fotovolt_Curral_Novo_Consolidado.xlsx` é a de decisão (dinheiro + energia + retorno),
  `financeiro/LF_Agropastoril_Analise_Relatorios_2026.xlsx` é a operacional (detalhe por cliente).
- O repasse de uma competência entra na conta da SPE no mês seguinte. Sempre conciliar com essa defasagem.
- A TIR realizada é negativa porque o payback não fechou. Nunca apresentar esse número sozinho:
  vem sempre junto da TIR projetada da aba Cenarios.
- O conhecimento das empresas fica em `empresas/`, em markdown, no formato Entity Overview.
- Dinheiro sempre conferido contra o rodapé do PDF de origem. Nunca digitar número à mão.
- Números estimados (tributos, produtividade de kWp) ficam em célula azul, editável,
  e são sempre marcados como estimativa a confirmar com o contador.
