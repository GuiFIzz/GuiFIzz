import json
from openpyxl import load_workbook
R=json.load(open("ref.json")); NM=len(json.load(open("dados.json"))["meta"])
OUT="/home/user/GuiFIzz/financeiro/LF_Agropastoril_Analise_Relatorios_2026.xlsx"
wb=load_workbook(OUT)
c=wb["Contrato_Bro"]
c["A13"]=f"Faturamento bruto RECEBIDO dos consumidores ({NM} meses)"
c["A35"]="Remuneração total da locação (base de cálculo dos tributos)"
for cell,f in [("B14","=B13*0.10"),("D14","=C14-B14"),("B16","=C14+C15"),("B20","=B19*0.10"),
               ("B21","=B20-C14"),("B27","=B25*B26"),("B35","=B33+B34"),("B37","=B35-B36"),("B67","=B61")]:
    c[cell]=f
for r in range(41,46):
    c.cell(r,3).value=f"=$B$35*B{r}"; c.cell(r,4).value=f"=$B$36*B{r}"
for r in range(51,51+NM):
    c.cell(r,3).value="=$B$61*0.8"; c.cell(r,4).value=f"=IFERROR(B{r}/$B$61,0)"
wb["Indicadores"]["B22"]="=IFERROR(B21/B20-1,0)"
rel=wb["Relatorios"]
for r in range(5,5+NM):
    rel.cell(r,14).value=f'=IF(ABS(M{r}-L{r})<0.05,"OK","VERIFICAR")'
lm=wb["Leia-me"]
lm["A9"]=f"Clientes novos em {NM} relatórios"
from openpyxl.utils import get_column_letter
STATCOL=get_column_letter(5+NM); FATCOL=get_column_letter(6+NM)
lm["B9"]=f'=COUNTIF(Clientes_Comparativo!${STATCOL}$5:${STATCOL}$19,"NOVO*")'
wb["Indicadores"]["B19"]=f"=IFERROR(MAX(Clientes_Comparativo!${FATCOL}$5:${FATCOL}$19)/SUM(Clientes_Comparativo!${FATCOL}$5:${FATCOL}$19),0)"
lm["A6"]=f"Faturamento bruto emitido ({NM} meses)"
lm["A5"]=f"Repasse líquido recebido em {NM} meses"
wb.save(OUT); print("fix final aplicado")
