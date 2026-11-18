# Prompt — Planilha unificada Fotovolt Curral Novo

Cole este prompt junto com: (a) os relatórios mensais da Bro em PDF, (b) o extrato bancário
mais recente da SPE, (c) o contrato correto com a Bro Energy, quando existir.

---

Você é o CFO da Fotovolt Curral Novo SPE Ltda. Monte uma planilha única que una as duas
metades do negócio que hoje vivem separadas: a **energia** (relatórios mensais da Bro, em kWh)
e o **dinheiro** (extrato bancário da SPE, em reais). Hoje ninguém consegue responder quanto
cada kWh gerado virou de caixa no bolso de cada sócio — é isso que a planilha tem que resolver.

**Fontes e regras invioláveis**
- A fonte é sempre o documento original: PDFs dos relatórios e extrato bancário. Nunca digite
  número à mão; extraia e concilie. Todo total em dinheiro tem que bater com o rodapé do PDF
  de origem e com o saldo do extrato.
- O repasse de uma competência entra na conta da SPE no mês seguinte. Trate essa defasagem
  explicitamente e mostre a conciliação relatório para extrato, linha a linha.
- Premissa estimada (tributo, produtividade de kWp, taxa de desconto, CDI) fica em célula
  azul editável e marcada como estimativa a confirmar.
- Zero fórmulas quebradas. Valide antes de entregar.

**Entregue estas abas**

1. **Resumo executivo** — o estado do investimento em uma tela: capital investido, caixa gerado,
   payback real, TIR, quanto falta, e as três decisões que precisam ser tomadas agora.

2. **Conciliação energia e caixa** — por competência: kWh injetados, kWh compensados, faturado
   pela Bro, recebido pela Bro, administração retida, repasse, data de entrada no extrato,
   diferença. Uma linha de controle por mês dizendo se fecha ou não.

3. **Retorno do investimento** — fluxo de caixa real por sócio desde o primeiro aporte:
   TIR (XIRR) sobre as datas reais, payback simples e descontado, múltiplo sobre o capital,
   e comparação com o CDI no mesmo período (célula azul). O payback atual usa média histórica
   de distribuição; refaça com cenários voltados para frente.

4. **Conta corrente de sócios** — aportes, distribuições e saldo devido a cada um.
   Os quatro sócios têm 25% e aportaram R$ 90.000 cada, mas receberam valores diferentes
   (de R$ 52.333,04 a R$ 56.048,91). Mostre a diferença acumulada e quanto falta acertar.
   Trate separadamente a LF Agropastoril, que consta no QSA mas não aportou nem recebe.

5. **Caixa e sustentação** — saldo atual, custo fixo mensal, meses de fôlego, e a política de
   caixa mínimo que a empresa não tem. Mostre os aportes que os sócios tiveram que fazer para
   cobrir furos e quanto de distribuição deveria ter sido retida para evitá-los.

6. **Ativo e reposição** — CAPEX por kWp, idade da usina, vida útil de painéis e inversores,
   e a provisão mensal que deveria existir para trocar inversor. Um inversor já quebrou e não
   havia reserva. Calcule quanto deveria ser retido por mês para o próximo.

7. **Energia** — produção, consumo, resultado, estoque de créditos e a conciliação do saldo
   (a variação do estoque tem que bater com o resultado do mês; diferença acima de 1.000 kWh é
   crédito sumindo). Inclua o histórico por unidade consumidora.

8. **Carteira de clientes** — faturamento e consumo por instalação, entradas, saídas,
   concentração, desconto praticado por cliente e inadimplência por cliente.

9. **Cenários** — projeção de 24 meses com três cenários editáveis: pessimista, base e otimista,
   variando geração mensal, inadimplência e tamanho da carteira. Mostre o impacto de cada um na
   data do payback e na distribuição por sócio.

10. **Dashboard** — gráficos de produção contra consumo, receita contra distribuição, evolução
    do caixa, payback acumulado e consumo por cliente.

**Indicadores obrigatórios, todos calculados por fórmula**

Retorno: TIR por sócio e consolidada; payback simples e descontado; múltiplo sobre capital;
retorno anualizado real; prêmio sobre o CDI.

Unidade: R$ por kWh gerado; R$ por kWp investido; receita por kWp ao ano; custo fixo por kWh.

Eficiência: taxa de aproveitamento (compensado dividido por injetado); administração sobre
recebido; carga tributária sobre receita; despesa operacional sobre receita; margem de
distribuição.

Risco: concentração do maior cliente; inadimplência real por mês; meses de caixa; dependência
do estoque de créditos; receita em risco se o maior cliente sair.

Operação: produção por mês contra a média; meses abaixo de 80%; energia não gerada por
indisponibilidade e a receita que ela custou.

**Ao final**, escreva em texto: o que mudou desde a última versão, os três números que mais
importam, e o que precisa de decisão de sócio — separando o que é dinheiro já perdido do que
ainda dá para recuperar.
