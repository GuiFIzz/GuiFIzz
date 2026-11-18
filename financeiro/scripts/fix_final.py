# -*- coding: utf-8 -*-
"""Correções pós-build que dependem do layout final da planilha.

Localiza as linhas pelo RÓTULO, nunca pelo número, para não quebrar quando
um bloco novo desloca a aba. Faz parte da cadeia do atualizar.py.
"""
import json
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

R=json.load(open("ref.json")); NM=len(json.load(open("dados.json"))["meta"])
OUT="../LF_Agropastoril_Analise_Relatorios_2026.xlsx"
wb=load_workbook(OUT)
c=wb["Contrato_Bro"]

def acha(txt, col=1, ate=120):
    for r in range(1,ate):
        v=c.cell(r,col).value
        if isinstance(v,str) and txt.lower() in v.lower(): return r
    raise SystemExit(f"rótulo não encontrado em Contrato_Bro: {txt}")

FB =acha("Faturamento bruto RECEBIDO")
TA =acha("Taxa de Administração — 10%")
TI =acha("Taxa Inicial — 50%")
TOT=acha("Total retido pela Bro")
FE =acha("Faturamento total EMITIDO")
DEZ=acha("10% sobre o emitido")
EXP=acha("EXPOSIÇÃO se a Bro")
PF =acha("Parcela Fixa mensal prevista")
MA =acha("Meses analisados")
VL =acha("deveria ter sido faturado como LOCAÇÃO")
CP =acha("Contribuições pagas pelos consumidores")
CD =acha("Custos da Distribuidora")
RT =acha("REMUNERAÇÃO TOTAL")
VE =acha("efetivamente entrou na conta")
DIF=acha("Diferença entre a base tributável")
PIS=acha("PIS (cumulativo)")
MP =acha("Média do período")
GM =acha("Geração média mensal observada")

c.cell(FB,1).value=f"Faturamento bruto RECEBIDO dos consumidores ({NM} meses)"
c.cell(RT,1).value="Remuneração total da locação (base de cálculo dos tributos)"  # não pode começar com "="
c.cell(TA,2).value=f"=B{FB}*0.10"
c.cell(TA,4).value=f"=C{TA}-B{TA}"
c.cell(TOT,2).value=f"=C{TA}+C{TI}"
c.cell(DEZ,2).value=f"=B{FE}*0.10"
c.cell(EXP,2).value=f"=B{DEZ}-C{TA}"
c.cell(VL,2).value=f"=B{PF}*B{MA}"
c.cell(RT,2).value=f"=B{CP}+B{CD}"
c.cell(DIF,2).value=f"=B{RT}-B{VE}"
for r in range(PIS,PIS+5):
    c.cell(r,3).value=f"=$B${RT}*B{r}"
    c.cell(r,4).value=f"=$B${VE}*B{r}"
for r in range(MP-NM,MP):
    c.cell(r,3).value=f"=$B${MP}*0.8"
    c.cell(r,4).value=f"=IFERROR(B{r}/$B${MP},0)"
c.cell(GM,2).value=f"=B{MP}"

wb["Indicadores"]["B22"]="=IFERROR(B21/B20-1,0)"
rel=wb["Relatorios"]
for r in range(5,5+NM):
    rel.cell(r,14).value=f'=IF(ABS(M{r}-L{r})<0.05,"OK","VERIFICAR")'
STATCOL=get_column_letter(5+NM); FATCOL=get_column_letter(6+NM)
lm=wb["Leia-me"]
lm["A5"]=f"Repasse líquido recebido em {NM} meses"
lm["A6"]=f"Faturamento bruto emitido ({NM} meses)"
lm["A9"]=f"Clientes novos em {NM} relatórios"
lm["B9"]=f'=COUNTIF(Clientes_Comparativo!${STATCOL}$5:${STATCOL}$19,"NOVO*")'
wb["Indicadores"]["B19"]=f"=IFERROR(MAX(Clientes_Comparativo!${FATCOL}$5:${FATCOL}$19)/SUM(Clientes_Comparativo!${FATCOL}$5:${FATCOL}$19),0)"
wb.save(OUT); print(f"fix final por rótulo aplicado (Contrato_Bro: FB={FB} RT={RT} MP={MP})")
